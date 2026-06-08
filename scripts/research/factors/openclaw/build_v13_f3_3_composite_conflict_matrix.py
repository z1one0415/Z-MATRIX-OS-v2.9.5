#!/usr/bin/env python3
"""V13.F3.3 — Stage C: composite conflict matrix."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_3_composite_conflict_matrix.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-COMPOSITE-CONFLICT-MATRIX",
    "status": "V13_F3_3_COMPOSITE_CONFLICT_MATRIX_BUILT",
    "factor_pairs_reviewed": [["F04","F10"],["F04","F11"],["F10","F11"]],
    "pairwise_conflicts": [
        {"pair": ["F04","F10"], "conflict_type": "MOMENTUM_VS_DEFENSIVE_REGIME",
         "conflict_level": "MEDIUM", "resolution_rule": "REGIME_GATE_CONTROLS_F10_ACTIVATION"},
        {"pair": ["F04","F11"], "conflict_type": "MOMENTUM_VS_SHORT_REVERSAL",
         "conflict_level": "MEDIUM", "resolution_rule": "HORIZON_SEPARATION_AND_COST_GATE"},
        {"pair": ["F10","F11"], "conflict_type": "DEFENSIVE_LOW_VOL_VS_TACTICAL_REVERSAL",
         "conflict_level": "LOW", "resolution_rule": "F11_DISABLED_IF_COST_TURNOVER_GATE_FAILS"}
    ],
    "composite_execution_allowed": False, "weight_optimization_allowed": False,
    "alpha_claim_allowed": False
}, indent=2))
print("[F3.3-C] Conflict matrix built")
sys.exit(0)
