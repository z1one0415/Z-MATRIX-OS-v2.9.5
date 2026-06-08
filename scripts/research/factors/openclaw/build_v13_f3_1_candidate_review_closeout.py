#!/usr/bin/env python3
"""V13.F3.1 — Stage H: candidate review closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
sc = json.loads((BATCH / "v13_f3_1_candidate_review_scorecard.json").read_text())
freeze = sc.get("candidate_freeze_ready", [])
tactical = sc.get("tactical_candidate_ready", [])
oos = sc.get("needs_oos_factors", [])
rework_f = sc.get("rework_required_factors", [])
reject_f = sc.get("rejected_factors", [])
ready_f3_2 = sc.get("ready_for_f3_2_candidate_freeze_review", [])

if ready_f3_2:
    next_action = "PREPARE_V13_F3_2_CANDIDATE_FREEZE_REVIEW"
elif oos:
    next_action = "PREPARE_V13_F3_1_1_TRUE_OOS_REQUIREMENT_PLAN"
else:
    next_action = "CONTINUE_OPENCLAW_PARALLEL_FACTOR_BATCH_DISCOVERY"

(BATCH / "v13_f3_1_candidate_review_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-1-CANDIDATE-REVIEW-CLOSEOUT",
    "status": "V13_F3_1_CANDIDATE_REVIEW_PASS" if ready_f3_2 else "V13_F3_1_CANDIDATE_REVIEW_BLOCKED",
    "base_commit": "337dbb5",
    "candidate_review_executed": True,
    "reviewed_factors": ["F04", "F10", "F11"],
    "candidate_freeze_ready": freeze,
    "tactical_candidate_ready": tactical,
    "needs_oos_factors": oos,
    "rework_required_factors": rework_f,
    "rejected_factors": reject_f,
    "ready_for_f3_2_candidate_freeze_review": ready_f3_2,
    "ready_for_promotion_review": [],
    "promotion_review_allowed": False,
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "oos_alpha_validation_executed": False, "skillos_protocol_modified": False,
    "frontend_modified": False, "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": next_action
}, indent=2))
print(f"[F3.1-H] Closeout: freeze={freeze} tactical={tactical} ready_f3_2={ready_f3_2} next={next_action}")
sys.exit(0)
