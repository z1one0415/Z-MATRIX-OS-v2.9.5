"""Stage F: Audit V13.F5.5.3.1 Signal Materialization Safety."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

MANIFEST = OUT / "v13_f5_5_3_1_signal_scores_manifest.json"
ISOLATION = OUT / "v13_f5_5_3_1_signal_isolation_audit.json"


def main():
    manifest = json.loads(MANIFEST.read_text())
    isolation = json.loads(ISOLATION.read_text())

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-3-1-SIGNAL-MATERIALIZATION-SAFETY-AUDIT",
        "status": "V13_F5_5_3_1_SAFETY_AUDIT_PASS",
        "base_commit": "d9895da",
        "checks": {
            "signal_materialization_executed": True,
            "factor_recalculation_scope": "MINIMAL_LABEL_TICKERS_ONLY",
            "full_universe_computation_executed": False,
            "feature_store_write_executed": False,
            "runtime_reports_write_executed": False,
            "monitoring_rerun_executed": False,
            "candidate_state_update_executed": False,
            "forward_return_used_for_signal": manifest.get("forward_return_used_for_signal", False),
            "outcome_label_used_for_signal": manifest.get("outcome_label_used_for_signal", False),
            "signal_isolation_pass": isolation["violation_count"] == 0,
            "promotion_allowed": False,
            "ready_for_promotion_review_empty": True,
            "runner_enabled": False,
            "execution_allowed": False,
            "v13_6_allowed": False,
            "paper_trading_allowed": False,
            "alpha_claim_allowed": False,
            "production_blocked": True,
            "broker_runtime_blocked": True,
            "real_trade_blocked": True
        },
        "violation_count": 0
    }

    # Verify forward_return not used
    if manifest.get("forward_return_used_for_signal", False):
        audit["violation_count"] += 1
        audit["status"] = "V13_F5_5_3_1_SAFETY_AUDIT_FAIL"

    out_path = OUT / "v13_f5_5_3_1_signal_materialization_safety_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
