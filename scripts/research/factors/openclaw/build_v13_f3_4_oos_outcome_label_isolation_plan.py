#!/usr/bin/env python3
"""V13.F3.4 — Stage D: OOS outcome label isolation plan."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_4_oos_outcome_label_isolation_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-OOS-OUTCOME-LABEL-ISOLATION-PLAN",
    "status": "V13_F3_4_OOS_OUTCOME_LABEL_ISOLATION_PLAN_BUILT",
    "label_generation_executed": False,
    "label_role": "TRUE_OOS_OUTCOME_LABEL_ONLY",
    "label_horizons": ["5D","20D","60D"],
    "label_panel_write_to_factor_panel_allowed": False,
    "label_panel_write_to_composite_panel_allowed": False,
    "required_label_columns": ["oos_rebalance_date","ticker","forward_return_5d","forward_return_20d","forward_return_60d","label_known_after_rebalance","label_role"],
    "forbidden_in_factor_panels": ["forward_return_5d","forward_return_20d","forward_return_60d","future_return","target_return","label"],
    "feature_label_leakage_forbidden": True, "true_oos_validation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.4-D] OOS label isolation plan built")
sys.exit(0)
