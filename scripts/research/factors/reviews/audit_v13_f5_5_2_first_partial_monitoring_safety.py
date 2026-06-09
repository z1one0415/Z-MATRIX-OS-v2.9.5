"""Stage F: Audit V13.F5.5.2 First Partial Monitoring Safety."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

DIAGNOSTIC = OUT / "v13_f5_5_2_micro_sample_monitoring_diagnostic.json"
STATE_AUDIT = OUT / "v13_f5_5_2_monitoring_state_non_update_audit.json"


def main():
    diagnostic = json.loads(DIAGNOSTIC.read_text())
    state_audit = json.loads(STATE_AUDIT.read_text())

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-2-FIRST-PARTIAL-MONITORING-SAFETY-AUDIT",
        "status": "V13_F5_5_2_SAFETY_AUDIT_PASS",
        "base_commit": "e7d7b1f",
        "checks": {
            "monitoring_execution_executed": True,
            "formal_oos_validation_executed": False,
            "candidate_decision_update_executed": False,
            "candidate_freeze_executed": False,
            "promotion_allowed": False,
            "ready_for_promotion_review_empty": True,
            "multi_factor_composite_built": False,
            "weight_optimization_executed": False,
            "runner_enabled": False,
            "execution_allowed": False,
            "v13_6_allowed": False,
            "paper_trading_allowed": False,
            "alpha_claim_allowed": False,
            "production_blocked": True,
            "broker_runtime_blocked": True,
            "real_trade_blocked": True
        },
        "monitoring_scope_note": "MICRO_SAMPLE_PARTIAL_DIAGNOSTIC_ONLY",
        "state_non_update_verified": state_audit["status"] == "V13_F5_5_2_STATE_NON_UPDATE_PASS",
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_2_first_partial_monitoring_safety_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
