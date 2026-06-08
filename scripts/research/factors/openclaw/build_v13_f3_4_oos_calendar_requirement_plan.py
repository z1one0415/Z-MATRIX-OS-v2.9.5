#!/usr/bin/env python3
"""V13.F3.4 — Stage C: OOS calendar requirement."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_4_oos_calendar_requirement_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-OOS-CALENDAR-REQUIREMENT-PLAN",
    "status": "V13_F3_4_OOS_CALENDAR_REQUIREMENT_PLAN_BUILT",
    "rebalance_frequency": "MONTHLY",
    "candidate_scope": ["F04","F10","F11"],
    "minimum_true_oos_rebalance_months_required": 6,
    "preferred_true_oos_rebalance_months_required": 12,
    "minimum_cross_section_coverage_tier": "U475",
    "minimum_covered_ticker_count": 475,
    "oos_calendar_generation_executed": False, "oos_validation_executed": False,
    "blocked_if_oos_months_below_minimum": True,
    "blocked_if_coverage_below_u475": True,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.4-C] OOS calendar plan built")
sys.exit(0)
