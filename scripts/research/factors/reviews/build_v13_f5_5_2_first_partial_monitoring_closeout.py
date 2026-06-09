"""Stage G: Build V13.F5.5.2 First Partial Monitoring Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

INPUT_AUDIT = OUT / "v13_f5_5_2_monitoring_input_audit.json"
SIGNAL_AUDIT = OUT / "v13_f5_5_2_factor_signal_availability_audit.json"
DIAGNOSTIC = OUT / "v13_f5_5_2_micro_sample_monitoring_diagnostic.json"
STATE_AUDIT = OUT / "v13_f5_5_2_monitoring_state_non_update_audit.json"
SAFETY_AUDIT = OUT / "v13_f5_5_2_first_partial_monitoring_safety_audit.json"


def main():
    input_audit = json.loads(INPUT_AUDIT.read_text())
    signal_audit = json.loads(SIGNAL_AUDIT.read_text())
    diagnostic = json.loads(DIAGNOSTIC.read_text())
    state_audit = json.loads(STATE_AUDIT.read_text())
    safety_audit = json.loads(SAFETY_AUDIT.read_text())

    all_pass = (
        "PASS" in input_audit["status"] and
        state_audit["violation_count"] == 0 and
        safety_audit["violation_count"] == 0
    )

    label_coverage = diagnostic["label_coverage"]

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-2-FIRST-PARTIAL-MONITORING-CLOSEOUT",
        "status": ("V13_F5_5_2_FIRST_PARTIAL_MONITORING_PASS" if all_pass
                   else "V13_F5_5_2_FIRST_PARTIAL_MONITORING_BLOCKED"),
        "base_commit": "e7d7b1f",
        "monitoring_execution_executed": True,
        "monitoring_execution_scope": "MICRO_SAMPLE_PARTIAL_DIAGNOSTIC_ONLY",
        "label_month": "2026-05",
        "label_data_row_count": label_coverage["total_label_rows"],
        "ticker_count": label_coverage["usable_ticker_count"],
        "generated_horizons_used": ["5D", "20D"],
        "blocked_horizons": ["60D"],
        "factor_signals_available": signal_audit["factors_with_signal_available"],
        "factor_signals_blocked": signal_audit["factors_with_signal_blocked"],
        "directional_spread_computed": signal_audit["factors_with_signal_available"] > 0,
        "formal_oos_validation_executed": False,
        "formal_statistical_inference_allowed": False,
        "candidate_state_update_executed": False,
        "suspension_decision_executed": False,
        "rejection_decision_executed": False,
        "promotion_allowed": False,
        "ready_for_promotion_review": [],
        "runner_enabled": False,
        "execution_allowed": False,
        "v13_6_allowed": False,
        "paper_trading_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "recommended_next_action": "PREPARE_V13_F5_5_3_MONITORING_SAMPLE_EXPANSION_OR_NEXT_OOS_MONTH_PLAN"
    }

    out_path = OUT / "v13_f5_5_2_first_partial_monitoring_closeout.json"
    out_path.write_text(json.dumps(closeout, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Status: {closeout['status']}")
    print(f"Factor signals: {closeout['factor_signals_available']} available, "
          f"{closeout['factor_signals_blocked']} blocked")


if __name__ == "__main__":
    main()
