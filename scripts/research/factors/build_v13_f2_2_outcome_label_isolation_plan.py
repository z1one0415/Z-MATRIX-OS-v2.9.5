#!/usr/bin/env python3
"""V13.F2.2 — Stage C: outcome label isolation planning."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

plan = {
    "pipeline_signature": "Z2-V13-F2-2-OUTCOME-LABEL-ISOLATION",
    "status": "V13_F2_2_OUTCOME_LABEL_ISOLATION_PLAN_BUILT",
    "label_generation_executed": False,
    "label_generation_allowed_next_step": True,
    "label_role": "OUTCOME_LABEL_ONLY",
    "label_horizons": ["20D", "60D"],
    "label_source": "real_price_bars_after_rebalance_date",
    "feature_panel_write_allowed": False,
    "feature_panel_contains_outcome_labels": False,
    "label_panel_output_planned": "runtime_reports/research/factors/single_factor_outcome_label_panel.csv",
    "required_label_columns": [
        "rebalance_date",
        "ticker",
        "forward_return_20d",
        "forward_return_60d",
        "label_known_after_rebalance",
        "label_role"
    ],
    "forbidden_in_factor_panels": [
        "forward_return_20d",
        "forward_return_60d",
        "future_return",
        "target_return",
        "label"
    ],
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_2_outcome_label_isolation_plan.json"
dst.write_text(json.dumps(plan, indent=2))
print(f"[F2.2-C] Outcome label isolation plan built -> {dst}")
sys.exit(0)
