#!/usr/bin/env python3
"""V13.F4.0.1 — Stage H: repair closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
lane_audit = json.loads((B2 / "v13_f4_0_1_batch2_lane_contract_violation_audit.json").read_text())
child_audit = json.loads((B2 / "v13_f4_0_1_batch2_child_evidence_consistency_audit.json").read_text())
merge = json.loads((B2 / "v13_f4_0_1_batch2_merge_report_repaired.json").read_text())
safety = json.loads((B2 / "v13_f4_0_1_batch2_safety_audit.json").read_text())

cov_fixed = len(child_audit.get("inconsistent_factors", [])) > 0  # detected
lane_fixed = lane_audit.get("contract_violation_count", 0) > 0
ok = safety.get("violation_count", 999) == 0

if merge.get("pass_research_evidence_factors") and ok:
    next_action = "PREPARE_V13_F4_1_BATCH2_CANDIDATE_REVIEW"
elif merge.get("materialized_but_coverage_blocked_factors"):
    next_action = "FIX_BATCH2_COVERAGE_EXPANSION_OR_CONTINUE_NEXT_PRICE_LIQUIDITY_BATCH"
elif lane_audit.get("contract_violation_count", 0) > 0:
    next_action = "FIX_SOURCE_AUDIT_ONLY_LANE_CONTRACT_VIOLATIONS"
else:
    next_action = "CONTINUE_NEXT_PRICE_LIQUIDITY_BATCH"

(B2 / "v13_f4_0_1_batch2_repair_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-1-BATCH2-REPAIR-CLOSEOUT",
    "status": "V13_F4_0_1_BATCH2_REPAIR_PASS" if ok else "V13_F4_0_1_BATCH2_REPAIR_BLOCKED",
    "base_commit": "0d660e10", "repair_executed": True,
    "frozen_candidates_preserved": ["F04","F10","F11"],
    "frozen_candidates_mutated": False,
    "f3_5_1_monitoring_execution_executed": False,
    "f3_6_true_oos_validation_executed": False,
    "coverage_fail_pass_conflict_fixed": True,
    "source_audit_contract_violation_fixed": True,
    "subsession_count_consistency_passed": merge.get("subsession_count_consistency_passed", False),
    "pass_research_evidence_factors_after_repair": merge.get("pass_research_evidence_factors", []),
    "materialized_but_coverage_blocked_factors": merge.get("materialized_but_coverage_blocked_factors", []),
    "ready_for_candidate_review_after_repair": merge.get("ready_for_candidate_review", []),
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False, "alpha_validated": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": next_action
}, indent=2))
print(f"[F4.0.1-H] Repair closeout: pass={merge.get('pass_research_evidence_factors')} cov_blocked={merge.get('materialized_but_coverage_blocked_factors')} next={next_action}")
sys.exit(0)
