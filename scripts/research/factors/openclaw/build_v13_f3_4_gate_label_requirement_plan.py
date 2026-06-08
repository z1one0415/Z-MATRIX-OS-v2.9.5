#!/usr/bin/env python3
"""V13.F3.4 — Stage E: gate label requirement plan."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_4_gate_label_requirement_plan.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-GATE-LABEL-REQUIREMENT-PLAN",
    "status": "V13_F3_4_GATE_LABEL_REQUIREMENT_PLAN_BUILT",
    "gates": [
        {"gate_id": "REGIME_GATE_FOR_F10", "applies_to": ["F10"],
         "required_oos_labels": ["market_return_20d","market_volatility_20d","drawdown_state","regime_state"],
         "lookahead_regime_label_forbidden": True, "gate_execution_executed": False},
        {"gate_id": "COST_TURNOVER_GATE_FOR_F11", "applies_to": ["F11"],
         "required_oos_labels": ["estimated_turnover","round_trip_cost_bps","spread_proxy","cost_state"],
         "future_cost_estimate_forbidden": True, "gate_execution_executed": False},
        {"gate_id": "HORIZON_GATE", "applies_to": ["F04","F10","F11"],
         "required_oos_labels": ["target_horizon","factor_allowed_horizons"],
         "gate_execution_executed": False}
    ],
    "gate_execution_allowed_this_round": False, "true_oos_validation_executed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.4-E] Gate label plan built")
sys.exit(0)
