#!/usr/bin/env python3
"""V13.F3.3 — Stage D: composite gate design."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_3_composite_gate_design.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-COMPOSITE-GATE-DESIGN",
    "status": "V13_F3_3_COMPOSITE_GATE_DESIGN_BUILT",
    "gates": [
        {"gate_id": "REGIME_GATE_FOR_F10", "applies_to": ["F10"],
         "purpose": "Allow low-volatility signal only in suitable defensive regimes",
         "candidate_inputs": ["market_return_20d","market_volatility_20d","drawdown_state"],
         "execution_allowed": False, "requires_f3_4_oos_validation": True},
        {"gate_id": "COST_TURNOVER_GATE_FOR_F11", "applies_to": ["F11"],
         "purpose": "Block tactical reversal when cost/turnover overwhelms edge",
         "candidate_inputs": ["estimated_turnover","round_trip_cost_bps","spread_proxy"],
         "execution_allowed": False, "requires_f3_4_oos_validation": True},
        {"gate_id": "HORIZON_GATE", "applies_to": ["F04","F10","F11"],
         "purpose": "Prevent using factor outside frozen horizon scope",
         "candidate_inputs": ["target_horizon","factor_allowed_horizons"],
         "execution_allowed": False, "requires_f3_4_oos_validation": True}
    ],
    "gate_execution_allowed": False, "composite_execution_allowed": False,
    "alpha_claim_allowed": False
}, indent=2))
print("[F3.3-D] Gate design built")
sys.exit(0)
