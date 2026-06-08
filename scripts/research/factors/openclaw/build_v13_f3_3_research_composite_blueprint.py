#!/usr/bin/env python3
"""V13.F3.3 — Stage E: research composite blueprint."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_3_research_composite_blueprint.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-RESEARCH-COMPOSITE-BLUEPRINT",
    "status": "V13_F3_3_RESEARCH_COMPOSITE_BLUEPRINT_BUILT",
    "blueprint_name": "F04_F10_F11_RESEARCH_TRIAD_BLUEPRINT",
    "blueprint_only": True,
    "composite_formula_executable": False,
    "numeric_weights_assigned": False,
    "component_roles": {"F04": "CORE_FULL_HORIZON", "F10": "REGIME_DEFENSIVE", "F11": "TACTICAL_REVERSAL"},
    "activation_logic_design": [
        "F04 active as core research signal",
        "F10 active only if regime gate passes",
        "F11 active only if cost/turnover gate passes",
        "No component may activate outside frozen horizon scope"
    ],
    "forbidden_outputs": ["composite_factor_value","portfolio_weight","trade_signal","position","order","broker_instruction"],
    "ready_for_f3_4_true_oos_requirement_plan": True,
    "ready_for_f3_5_candidate_monitoring_plan": True,
    "promotion_allowed": False, "v13_6_allowed": False, "alpha_claim_allowed": False
}, indent=2))
print("[F3.3-E] Blueprint built")
sys.exit(0)
