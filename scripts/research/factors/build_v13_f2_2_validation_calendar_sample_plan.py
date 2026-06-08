#!/usr/bin/env python3
"""V13.F2.2 — Stage D: validation calendar / sample sufficiency planning."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

plan = {
    "pipeline_signature": "Z2-V13-F2-2-CALENDAR-SAMPLE",
    "status": "V13_F2_2_VALIDATION_CALENDAR_SAMPLE_PLAN_BUILT",
    "rebalance_frequency": "MONTHLY",
    "candidate_rebalance_dates_source": "F03_F06_PANEL_INTERSECTION",
    "minimum_month_count_required": 12,
    "preferred_month_count_required": 24,
    "minimum_cross_section_ticker_count": 100,
    "sample_sufficiency_checked_this_round": False,
    "sample_sufficiency_check_allowed_next_step": True,
    "validation_horizons": ["20D", "60D"],
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_2_validation_calendar_sample_plan.json"
dst.write_text(json.dumps(plan, indent=2))
print(f"[F2.2-D] Calendar/sample plan built -> {dst}")
sys.exit(0)
