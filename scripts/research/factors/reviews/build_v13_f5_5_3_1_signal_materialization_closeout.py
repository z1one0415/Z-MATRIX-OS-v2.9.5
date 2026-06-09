"""Stage G: Build V13.F5.5.3.1 Signal Materialization Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

MANIFEST = OUT / "v13_f5_5_3_1_signal_scores_manifest.json"
ISOLATION = OUT / "v13_f5_5_3_1_signal_isolation_audit.json"
COVERAGE = OUT / "v13_f5_5_3_1_signal_coverage_validation.json"
SAFETY = OUT / "v13_f5_5_3_1_signal_materialization_safety_audit.json"


def main():
    manifest = json.loads(MANIFEST.read_text())
    isolation = json.loads(ISOLATION.read_text())
    coverage = json.loads(COVERAGE.read_text())
    safety = json.loads(SAFETY.read_text())

    all_pass = (
        isolation["violation_count"] == 0 and
        coverage.get("all_eligible_factors_complete", False) and
        safety["violation_count"] == 0
    )

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-3-1-SIGNAL-MATERIALIZATION-CLOSEOUT",
        "status": ("V13_F5_5_3_1_MINIMAL_SIGNAL_SCORE_MATERIALIZATION_PASS" if all_pass
                   else "V13_F5_5_3_1_MINIMAL_SIGNAL_SCORE_MATERIALIZATION_BLOCKED"),
        "base_commit": "d9895da",
        "signal_materialization_executed": True,
        "materialized_factors": manifest["materialized_factors"],
        "blocked_factors": ["F04", "F10", "F11", "F14", "F15", "F16",
                            "F22", "F26", "F27", "F34"],
        "rebalance_date": manifest["rebalance_date"],
        "ticker_count": manifest["ticker_count"],
        "rows_per_factor": manifest["rows_per_factor"],
        "total_signal_rows": manifest["total_signal_rows"],
        "signal_role": manifest["signal_role"],
        "full_universe_computation_executed": False,
        "feature_store_write_executed": False,
        "runtime_reports_write_executed": False,
        "monitoring_rerun_executed": False,
        "candidate_state_update_executed": False,
        "ready_for_f5_5_2_rerun_partial_4_factor": all_pass,
        "ready_for_full_10_factor_monitoring": False,
        "ready_for_promotion_review": [],
        "promotion_allowed": False,
        "runner_enabled": False,
        "execution_allowed": False,
        "v13_6_allowed": False,
        "paper_trading_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "recommended_next_action": "PREPARE_V13_F5_5_2_1_RERUN_PARTIAL_MONITORING_FOR_4_SIGNAL_READY_FACTORS"
    }

    out_path = OUT / "v13_f5_5_3_1_signal_materialization_closeout.json"
    out_path.write_text(json.dumps(closeout, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Status: {closeout['status']}")
    print(f"Total signal rows: {closeout['total_signal_rows']}")
    print(f"Ready for F5.5.2 rerun: {closeout['ready_for_f5_5_2_rerun_partial_4_factor']}")


if __name__ == "__main__":
    main()
