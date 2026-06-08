#!/usr/bin/env python3
"""V13.F3.5 — Stage G: F3.6 handoff plan."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_to_f3_6_true_oos_handoff_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-TO-F3-6-TRUE-OOS-HANDOFF-PLAN",
    "status": "V13_F3_5_TO_F3_6_TRUE_OOS_HANDOFF_PLAN_BUILT",
    "handoff_allowed_only_when": {
        "minimum_true_oos_months_available": 6,
        "preferred_true_oos_months_available": 12,
        "coverage_tier": "U475",
        "oos_labels_isolated": True,
        "monitoring_state_not_suspended": True,
        "same_sample_reuse_blocked": True
    },
    "ready_for_f3_6_now": False, "true_oos_validation_executed": False,
    "oos_label_generation_executed": False, "promotion_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.5-G] F3.6 handoff plan built")
sys.exit(0)
