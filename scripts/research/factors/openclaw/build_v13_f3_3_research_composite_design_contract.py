#!/usr/bin/env python3
"""V13.F3.3 — Stage A: design contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_3_research_composite_design_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-3-RESEARCH-COMPOSITE-DESIGN-CONTRACT",
    "status": "V13_F3_3_RESEARCH_COMPOSITE_DESIGN_CONTRACT_BUILT",
    "base_commit": "c4d59ba", "design_only": True,
    "composite_execution_allowed": False, "composite_panel_generation_allowed": False,
    "weight_optimization_allowed": False,
    "candidate_scope": ["F04", "F10", "F11"],
    "candidate_roles": {"F04": "CORE_FULL_HORIZON_SIGNAL", "F10": "REGIME_DEFENSIVE_SIGNAL", "F11": "TACTICAL_SHORT_HORIZON_SIGNAL"},
    "requires_true_oos_before_any_alpha_claim": True,
    "requires_f3_4_oos_plan_before_execution": True,
    "requires_f3_5_monitoring_plan_before_execution": True,
    "promotion_allowed": False, "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.3-A] Design contract built")
sys.exit(0)
