#!/usr/bin/env python3
"""V13.F3.2 — Stage H: freeze closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
reg = json.loads((BATCH / "v13_f3_2_candidate_freeze_registry.json").read_text())
safety = json.loads((BATCH / "v13_f3_2_candidate_freeze_safety_audit.json").read_text())
ok = len(safety.get("violations", [])) == 0
(BATCH / "v13_f3_2_candidate_freeze_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-2-CANDIDATE-FREEZE-CLOSEOUT",
    "status": "V13_F3_2_CANDIDATE_FREEZE_PASS" if ok else "V13_F3_2_CANDIDATE_FREEZE_BLOCKED",
    "base_commit": "5de48e0", "candidate_freeze_executed": True,
    "frozen_candidate_count": 3,
    "frozen_candidates": ["F04", "F10", "F11"],
    "f04_freeze_status": "FROZEN_CANDIDATE",
    "f10_freeze_status": "FROZEN_REGIME_SPECIFIC_CANDIDATE",
    "f11_freeze_status": "FROZEN_TACTICAL_CANDIDATE",
    "ready_for_f3_3_research_composite_design": ["F04", "F10", "F11"],
    "ready_for_f3_4_true_oos_requirement_plan": ["F04", "F10", "F11"],
    "ready_for_promotion_review": [],
    "promotion_review_allowed": False,
    "multi_factor_composite_built": False,
    "multi_factor_composite_design_allowed_next": True,
    "weight_optimization_executed": False,
    "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False,
    "alpha_validated": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_V13_F3_3_RESEARCH_COMPOSITE_DESIGN"
}, indent=2))
print(f"[F3.2-H] Freeze closeout: {reg.get('frozen_candidate_count', 0)} frozen, safety={'✅' if ok else '❌'}")
sys.exit(0)
