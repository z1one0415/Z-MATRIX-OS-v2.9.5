#!/usr/bin/env python3
"""V13.F3.4 — Stage A: OOS requirement contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(B / "v13_f3_4_true_oos_requirement_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-TRUE-OOS-REQUIREMENT-CONTRACT",
    "status": "V13_F3_4_TRUE_OOS_REQUIREMENT_CONTRACT_BUILT",
    "base_commit": "e6a3567", "requirement_plan_only": True,
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "composite_execution_allowed": False, "composite_panel_generation_allowed": False,
    "weight_optimization_allowed": False,
    "candidate_scope": ["F04","F10","F11"],
    "blueprint_scope": "F04_F10_F11_RESEARCH_TRIAD_BLUEPRINT",
    "minimum_true_oos_months_required": 6, "preferred_true_oos_months_required": 12,
    "same_sample_promotion_forbidden": True, "freeze_pre_sample_reuse_forbidden": True,
    "promotion_allowed": False, "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.4-A] OOS contract built")
sys.exit(0)
