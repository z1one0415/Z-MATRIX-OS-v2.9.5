"""Stage G: Build V13.F5.5.4.1 Signal Materialization Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

MANIFEST = OUT / "v13_f5_5_4_1_signal_scores_manifest.json"
COVERAGE = OUT / "v13_f5_5_4_1_signal_coverage_validation.json"
SAFETY = OUT / "v13_f5_5_4_1_signal_materialization_safety_audit.json"

TARGET_FACTORS = ["F04", "F10", "F11", "F14", "F15", "F16"]
ALREADY_READY = ["F21", "F24", "F30", "F31"]


def main():
    manifest = json.loads(MANIFEST.read_text())
    coverage = json.loads(COVERAGE.read_text())
    safety = json.loads(SAFETY.read_text())

    materialized = manifest["materialized_factors"]
    blocked = manifest["blocked_factors"]
    total_signal_ready = len(ALREADY_READY) + len(materialized)
    all_10_ready = total_signal_ready == 10

    # Determine status
    if len(materialized) == 6:
        status = "V13_F5_5_4_1_SIGNAL_MATERIALIZATION_PASS"
    elif len(materialized) > 0:
        status = "V13_F5_5_4_1_SIGNAL_MATERIALIZATION_PARTIAL"
    else:
        status = "V13_F5_5_4_1_SIGNAL_MATERIALIZATION_BLOCKED"

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-4-1-BATCH1-BATCH2-SIGNAL-MATERIALIZATION-CLOSEOUT",
        "status": status,
        "base_commit": "7384266",
        "signal_materialization_executed": True,
        "target_factors": TARGET_FACTORS,
        "materialized_factors": materialized,
        "blocked_factors": blocked,
        "blocked_reasons": manifest.get("blocked_reasons", {}),
        "already_signal_ready": ALREADY_READY,
        "total_signal_ready_factors": total_signal_ready,
        "rebalance_date": manifest["rebalance_date"],
        "ticker_count": manifest["ticker_count"],
        "total_signal_rows_this_step": manifest["total_signal_rows"],
        "signal_role": "FACTOR_SIGNAL_ONLY",
        "full_universe_computation_executed": False,
        "feature_store_write_executed": False,
        "runtime_reports_write_executed": False,
        "monitoring_rerun_executed": False,
        "candidate_state_update_executed": False,
        "ready_for_10_factor_partial_monitoring": all_10_ready,
        "ready_for_7_factor_partial_monitoring": total_signal_ready >= 7,
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
        "recommended_next_action": (
            "PREPARE_V13_F5_5_2_2_RERUN_PARTIAL_MONITORING_FOR_10_SIGNAL_READY_FACTORS"
            if all_10_ready else
            "PREPARE_V13_F5_5_4_2_REPAIR_BLOCKED_SIGNAL_SOURCES_OR_RERUN_PARTIAL_AVAILABLE_FACTORS"
        )
    }

    (OUT / "v13_f5_5_4_1_signal_materialization_closeout.json").write_text(
        json.dumps(closeout, indent=2) + "\n")
    print(f"Written: closeout")
    print(f"Status: {status}")
    print(f"Materialized: {materialized}, Blocked: {blocked}")
    print(f"Total signal-ready: {total_signal_ready}/10")
    print(f"Ready for 10-factor monitoring: {all_10_ready}")


if __name__ == "__main__":
    main()
