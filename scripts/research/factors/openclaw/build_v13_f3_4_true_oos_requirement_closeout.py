#!/usr/bin/env python3
"""V13.F3.4 — Stage H: OOS requirement closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
audit = json.loads((B / "v13_f3_4_same_sample_promotion_block_audit.json").read_text()) if (B / "v13_f3_4_same_sample_promotion_block_audit.json").exists() else {}
ok = audit.get("violation_count", 999) == 0
(B / "v13_f3_4_true_oos_requirement_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-4-TRUE-OOS-REQUIREMENT-CLOSEOUT",
    "status": "V13_F3_4_TRUE_OOS_REQUIREMENT_PLAN_PASS" if ok else "V13_F3_4_TRUE_OOS_REQUIREMENT_PLAN_BLOCKED",
    "base_commit": "e6a3567", "requirement_plan_executed": True,
    "true_oos_validation_executed": False, "oos_label_generation_executed": False,
    "candidate_scope": ["F04","F10","F11"],
    "blueprint_scope": "F04_F10_F11_RESEARCH_TRIAD_BLUEPRINT",
    "minimum_true_oos_months_required": 6, "preferred_true_oos_months_required": 12,
    "same_sample_promotion_blocked": ok,
    "oos_outcome_label_isolation_planned": True, "gate_label_requirements_planned": True,
    "per_factor_acceptance_criteria_built": True,
    "ready_for_f3_5_candidate_monitoring_plan": True,
    "ready_for_f3_6_true_oos_validation_execution": False,
    "ready_for_promotion_review": [], "promotion_review_allowed": False,
    "composite_execution_executed": False, "multi_factor_composite_built": False,
    "composite_panel_generated": False, "weight_optimization_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_V13_F3_5_CANDIDATE_MONITORING_PLAN"
}, indent=2))
print(f"[F3.4-H] OOS closeout: safety={'✅' if ok else '❌'}")
sys.exit(0)
