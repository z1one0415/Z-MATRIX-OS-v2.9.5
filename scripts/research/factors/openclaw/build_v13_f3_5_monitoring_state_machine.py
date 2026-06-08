#!/usr/bin/env python3
"""V13.F3.5 — Stage D: monitoring state machine."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_5_monitoring_state_machine.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-5-MONITORING-STATE-MACHINE",
    "status": "V13_F3_5_MONITORING_STATE_MACHINE_BUILT",
    "states": ["FROZEN","RETAINED","WATCH","ORANGE","SUSPENSION_REVIEW","SUSPENDED","REWORK_REQUIRED","REJECTED"],
    "allowed_transitions": [
        {"from":"FROZEN","to":"RETAINED"},{"from":"RETAINED","to":"WATCH"},{"from":"WATCH","to":"ORANGE"},
        {"from":"ORANGE","to":"SUSPENSION_REVIEW"},{"from":"SUSPENSION_REVIEW","to":"SUSPENDED"},
        {"from":"SUSPENDED","to":"REWORK_REQUIRED"},{"from":"REWORK_REQUIRED","to":"REJECTED"},
        {"from":"WATCH","to":"RETAINED"},{"from":"ORANGE","to":"WATCH"}
    ],
    "state_decision_basis": ["monthly_rank_ic","bucket_spread","cost_adjusted_spread","regime_gate_result","cost_turnover_gate_result","coverage_tier","data_quality"],
    "promotion_state_absent": True, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.5-D] State machine built")
sys.exit(0)
