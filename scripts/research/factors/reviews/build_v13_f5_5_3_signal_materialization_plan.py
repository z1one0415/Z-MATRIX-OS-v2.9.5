"""Stage E: Build V13.F5.5.3 Signal Materialization Plan."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")
OUT.mkdir(parents=True, exist_ok=True)

CLASSIFICATION = OUT / "v13_f5_5_3_signal_source_classification.json"
SCHEMA = OUT / "v13_f5_5_3_signal_score_schema.json"


def main():
    classification = json.loads(CLASSIFICATION.read_text())
    schema = json.loads(SCHEMA.read_text())

    eligible = classification["f5_5_3_1_eligible_factors"]
    blocked = classification["blocked_factors_requiring_prior_batch_work"]

    plan = {
        "pipeline_signature": "Z2-V13-F5-5-3-SIGNAL-MATERIALIZATION-PLAN",
        "status": "V13_F5_5_3_SIGNAL_MATERIALIZATION_PLAN_BUILT",
        "base_commit": "bfb48a7",
        "plan_structure": {
            "F5_5_3": "PLANNING_ONLY (current step - no materialization)",
            "F5_5_3_1": "MINIMAL_SIGNAL_SCORE_MATERIALIZATION (after human review)"
        },
        "f5_5_3_scope": "PLAN_AND_AUDIT_ONLY",
        "f5_5_3_1_scope": "MATERIALIZE_SIGNAL_SCORES_FOR_LABEL_TICKERS_ONLY",
        "f5_5_3_1_eligible_factors": eligible,
        "f5_5_3_1_blocked_factors": blocked,
        "f5_5_3_1_requirements": {
            "label_tickers_only": True,
            "rebalance_date": "2026-05-06",
            "signal_role": "FACTOR_SIGNAL_ONLY",
            "schema_ref": "v13_f5_5_3_signal_score_schema.json",
            "output_format": "one_csv_per_factor",
            "output_path_pattern": "research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization/{factor_id}_signal_scores.csv",
            "source_data_allowed": "data/price_bars (read-only)",
            "formula_source": "factor_manifest.formula_ref"
        },
        "f5_5_3_1_constraints": {
            "only_for_label_tickers": True,
            "only_for_rebalance_date": True,
            "no_full_universe_computation": True,
            "no_feature_store_write": True,
            "no_runtime_reports_write": True,
            "no_candidate_state_update": True,
            "no_trade_signal_output": True,
            "no_alpha_claim": True
        },
        "expected_output_after_f5_5_3_1": {
            "signal_scores_generated": len(eligible),
            "monitoring_rerun_eligible": len(eligible) > 0,
            "full_monitoring_eligible": len(eligible) == 10,
            "note": f"Only {len(eligible)}/10 factors can be materialized; "
                    f"{len(blocked)} require prior batch artifact work"
        },
        "signal_materialization_executed_in_f5_5_3": False,
        "factor_recalculation_executed": False,
        "monitoring_rerun_executed": False,
        "candidate_state_update_executed": False,
        "promotion_allowed": False,
        "runner_enabled": False,
        "execution_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED"
    }

    out_path = OUT / "v13_f5_5_3_signal_materialization_plan.json"
    out_path.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Eligible for F5.5.3.1: {len(eligible)}, Blocked: {len(blocked)}")


if __name__ == "__main__":
    main()
