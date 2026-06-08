#!/usr/bin/env python3
"""V13.F4.0 — Stage H: batch 2 closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
merge = json.loads((B2 / "v13_f4_0_batch2_merge_report.json").read_text())
safety = json.loads((B2 / "v13_f4_0_batch2_safety_audit.json").read_text())
pass_f = merge.get("pass_research_evidence_factors", [])
source_audit = merge.get("source_audit_only_completed", [])
safety_ok = safety.get("violation_count", 999) == 0

if pass_f and safety_ok:
    next_action = "PREPARE_V13_F4_1_BATCH2_CANDIDATE_REVIEW"
elif source_audit and not pass_f:
    next_action = "PREPARE_V13_F4_0_1_BATCH2_SOURCE_REPAIR_OR_NEXT_BATCH"
else:
    next_action = "PREPARE_V13_F4_0_1_BATCH2_SOURCE_REPAIR_OR_NEXT_BATCH"

(B2 / "v13_f4_0_batch2_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-BATCH2-CLOSEOUT",
    "status": "V13_F4_0_BATCH2_PASS" if safety_ok else "V13_F4_0_BATCH2_BLOCKED",
    "base_commit": "8f800b17",
    "batch2_orchestration_executed": True,
    "frozen_candidates_preserved": ["F04","F10","F11"],
    "frozen_candidates_mutated": False,
    "f3_5_1_monitoring_execution_executed": False,
    "f3_6_true_oos_validation_executed": False,
    "completed_subsessions": merge.get("completed_subsessions", 0),
    "pass_research_evidence_factors": pass_f,
    "ready_for_candidate_review": merge.get("ready_for_candidate_review", []),
    "source_audit_only_completed": source_audit,
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": next_action
}, indent=2))
print(f"[F4.0-H] Batch 2 closeout: pass={pass_f} source_audit={source_audit} next={next_action}")
sys.exit(0)
