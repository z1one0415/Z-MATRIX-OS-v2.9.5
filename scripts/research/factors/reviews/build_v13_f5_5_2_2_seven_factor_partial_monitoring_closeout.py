"""Stage G: V13.F5.5.2.2 Seven-Factor Partial Monitoring Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

DIAGNOSTIC = OUT / "v13_f5_5_2_2_seven_factor_directional_spread_diagnostic.json"
JOIN_AUDIT = OUT / "v13_f5_5_2_2_seven_factor_input_join_audit.json"
STATE_AUDIT = OUT / "v13_f5_5_2_2_state_non_update_audit.json"
SAFETY = OUT / "v13_f5_5_2_2_seven_factor_safety_audit.json"


def main():
    diagnostic = json.loads(DIAGNOSTIC.read_text())
    join_audit = json.loads(JOIN_AUDIT.read_text())
    state_audit = json.loads(STATE_AUDIT.read_text())
    safety = json.loads(SAFETY.read_text())

    all_pass = (
        join_audit["violation_count"] == 0 and
        state_audit["violation_count"] == 0 and
        safety["violation_count"] == 0 and
        diagnostic["summary"]["factors_with_spread_computed"] == 7
    )

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-2-2-SEVEN-FACTOR-PARTIAL-MONITORING-CLOSEOUT",
        "status": ("V13_F5_5_2_2_SEVEN_FACTOR_PARTIAL_MONITORING_PASS" if all_pass
                   else "V13_F5_5_2_2_SEVEN_FACTOR_PARTIAL_MONITORING_BLOCKED"),
        "base_commit": "ac96790",
        "seven_factor_partial_monitoring_executed": True,
        "monitoring_scope": ["F04", "F10", "F11", "F21", "F24", "F30", "F31"],
        "blocked_factors": ["F14", "F15", "F16"],
        "label_month": "2026-05",
        "rebalance_date": "2026-05-06",
        "ticker_count": 5,
        "label_rows": 10,
        "signal_rows": 35,
        "horizons_used": ["5D", "20D"],
        "directional_spread_computed": True,
        "factors_with_spread": diagnostic["summary"]["factors_with_spread_computed"],
        "factors_with_positive_5D_spread": diagnostic["summary"]["factors_with_positive_5D_spread"],
        "factors_with_positive_20D_spread": diagnostic["summary"]["factors_with_positive_20D_spread"],
        "sample_scope": "MICRO_SAMPLE_5_TICKERS",
        "formal_oos_validation_executed": False,
        "formal_statistical_inference_allowed": False,
        "candidate_state_update_executed": False,
        "suspension_decision_executed": False,
        "rejection_decision_executed": False,
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
        "recommended_next_action": "PREPARE_V13_F5_5_4_2_REPAIR_BLOCKED_SIGNAL_SOURCES_FOR_F14_F15_F16"
    }

    (OUT / "v13_f5_5_2_2_seven_factor_partial_monitoring_closeout.json").write_text(
        json.dumps(closeout, indent=2) + "\n")
    print(f"Written: closeout (status={closeout['status']})")
    print(f"Spread computed for {closeout['factors_with_spread']}/7 factors")


if __name__ == "__main__":
    main()
