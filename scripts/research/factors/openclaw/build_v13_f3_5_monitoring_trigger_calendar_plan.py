#!/usr/bin/env python3
"""V13.F3.5 — Stage F: monitoring trigger calendar plan."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_monitoring_trigger_calendar_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-MONITORING-TRIGGER-CALENDAR-PLAN",
    "status": "V13_F3_5_MONITORING_TRIGGER_CALENDAR_PLAN_BUILT",
    "monitoring_frequency": "MONTHLY",
    "minimum_oos_start_exclusive": "20260501",
    "first_eligible_monitoring_rebalance_rule": "first_month_end_rebalance_date_after_20260501_with_required_forward_labels_available",
    "label_availability_rules": [
        {"horizon":"5D","required_for":["F11"],"available_after_trading_days":5},
        {"horizon":"20D","required_for":["F04","F10","F11"],"available_after_trading_days":20},
        {"horizon":"60D","required_for":["F04","F10"],"available_after_trading_days":60}
    ],
    "monitoring_execution_executed": False, "true_oos_validation_executed": False,
    "oos_label_generation_executed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.5-F] Trigger calendar plan built")
sys.exit(0)
