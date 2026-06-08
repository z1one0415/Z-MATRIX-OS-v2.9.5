#!/usr/bin/env python3
"""V13.F3.3 — Stage B: composite role architecture."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_3_composite_role_architecture.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-COMPOSITE-ROLE-ARCHITECTURE",
    "status": "V13_F3_3_COMPOSITE_ROLE_ARCHITECTURE_BUILT",
    "composite_candidate_name": "F04_F10_F11_RESEARCH_TRIAD",
    "component_factors": [
        {"factor_id": "F04", "role": "CORE_SIGNAL", "candidate_type": "FULL_HORIZON_RESEARCH_CANDIDATE",
         "allowed_horizons": ["20D", "60D"], "activation_rule": "ALWAYS_ACTIVE_IN_RESEARCH_DESIGN",
         "weight_policy": "DESIGN_ONLY_NO_NUMERIC_WEIGHT"},
        {"factor_id": "F10", "role": "DEFENSIVE_REGIME_SIGNAL", "candidate_type": "REGIME_SPECIFIC_RESEARCH_CANDIDATE",
         "allowed_horizons": ["20D", "60D"], "activation_rule": "ACTIVE_ONLY_WHEN_REGIME_GATE_PASS",
         "required_gate": "REGIME_GATE", "weight_policy": "DESIGN_ONLY_NO_NUMERIC_WEIGHT"},
        {"factor_id": "F11", "role": "TACTICAL_SIGNAL", "candidate_type": "TACTICAL_RESEARCH_CANDIDATE",
         "allowed_horizons": ["5D", "20D"], "blocked_horizons": ["60D_FOR_STANDALONE_USE"],
         "activation_rule": "ACTIVE_ONLY_WHEN_COST_AND_TURNOVER_GATE_PASS",
         "required_gate": "COST_TURNOVER_GATE", "weight_policy": "DESIGN_ONLY_NO_NUMERIC_WEIGHT"}
    ],
    "numeric_weights_assigned": False, "composite_panel_generated": False,
    "multi_factor_composite_built": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.3-B] Role architecture built")
sys.exit(0)
