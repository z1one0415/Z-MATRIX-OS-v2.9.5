#!/usr/bin/env python3
"""V13.F2.3.1 — Stage E: F06 sample extension plan."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

plan = {
    "pipeline_signature": "Z2-V13-F2-3-1-F06-EXTENSION-PLAN",
    "status": "F06_SAMPLE_EXTENSION_PLAN_BUILT",
    "factor_id": "F06",
    "current_sample_month_count": 1,
    "minimum_month_count_required": 12,
    "preferred_month_count_required": 24,
    "required_extension_target": {
        "minimum_additional_months_needed": 11,
        "preferred_additional_months_needed": 23
    },
    "extension_methods_allowed": [
        "EXPAND_FUNDAMENTAL_HISTORY",
        "REBUILD_AVAILABLE_AT_MAPPING",
        "BACKFILL_DISCLOSURE_DATES",
        "REBUILD_REBALANCE_COVERAGE"
    ],
    "extension_methods_forbidden": [
        "SYNTHETIC_FUNDAMENTALS",
        "FORWARD_FILLED_FUTURE_STATEMENTS",
        "LOOKAHEAD_ANN_DATE",
        "OUTCOME_LABEL_IMPUTATION"
    ],
    "materialization_allowed_next_gate": True,
    "validation_allowed_after_extension": True,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "f06_fundamental_quality_sample_extension_plan.json"
dst.write_text(json.dumps(plan, indent=2))
print(f"[F2.3.1-E] F06 sample extension plan built -> {dst}")
sys.exit(0)
