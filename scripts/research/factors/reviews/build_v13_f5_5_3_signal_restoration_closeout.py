"""Stage G: Build V13.F5.5.3 Signal Restoration Closeout."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")
OUT.mkdir(parents=True, exist_ok=True)

CLASSIFICATION = OUT / "v13_f5_5_3_signal_source_classification.json"
PLAN = OUT / "v13_f5_5_3_signal_materialization_plan.json"
SAFETY = OUT / "v13_f5_5_3_signal_restoration_safety_audit.json"


def main():
    classification = json.loads(CLASSIFICATION.read_text())
    plan = json.loads(PLAN.read_text())
    safety = json.loads(SAFETY.read_text())

    safety_pass = safety["violation_count"] == 0
    plan_built = "BUILT" in plan["status"]

    all_pass = safety_pass and plan_built

    closeout = {
        "pipeline_signature": "Z2-V13-F5-5-3-SIGNAL-SCORE-RESTORATION-CLOSEOUT",
        "status": ("V13_F5_5_3_SIGNAL_SCORE_RESTORATION_PLAN_PASS" if all_pass
                   else "V13_F5_5_3_SIGNAL_SCORE_RESTORATION_PLAN_BLOCKED"),
        "base_commit": "bfb48a7",
        "planning_only": True,
        "current_signal_available_count": 0,
        "current_signal_blocked_count": 10,
        "factors_actionable_for_materialization": len(classification["f5_5_3_1_eligible_factors"]),
        "factors_blocked_no_source": len(classification["blocked_factors_requiring_prior_batch_work"]),
        "f5_5_3_1_eligible_factors": classification["f5_5_3_1_eligible_factors"],
        "restoration_plan_built": plan_built,
        "signal_materialization_executed": False,
        "factor_recalculation_executed": False,
        "monitoring_rerun_executed": False,
        "candidate_state_update_executed": False,
        "ready_for_f5_5_3_1_signal_score_materialization": all_pass and len(classification["f5_5_3_1_eligible_factors"]) > 0,
        "ready_for_f5_5_2_rerun": False,
        "ready_for_promotion_review": [],
        "promotion_allowed": False,
        "runner_enabled": False,
        "execution_allowed": False,
        "v13_6_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "recommended_next_action": "PREPARE_V13_F5_5_3_1_MINIMAL_SIGNAL_SCORE_MATERIALIZATION_FOR_EXISTING_LABEL_TICKERS"
    }

    out_path = OUT / "v13_f5_5_3_signal_restoration_closeout.json"
    out_path.write_text(json.dumps(closeout, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Status: {closeout['status']}")
    print(f"Eligible for F5.5.3.1: {closeout['factors_actionable_for_materialization']}")
    print(f"Ready for materialization: {closeout['ready_for_f5_5_3_1_signal_score_materialization']}")


if __name__ == "__main__":
    main()
