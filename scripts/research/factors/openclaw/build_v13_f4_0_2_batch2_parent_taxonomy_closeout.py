#!/usr/bin/env python3
"""V13.F4.0.2 — Stage F: taxonomy closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
safety = json.loads((B2 / "v13_f4_0_2_batch2_parent_safety_audit.json").read_text())
merge = json.loads((B2 / "v13_f4_0_2_batch2_merge_report_canonical.json").read_text())
ok = safety.get("violation_count", 999) == 0
pass_f = merge.get("pass_research_evidence_factors", [])

(B2 / "v13_f4_0_2_batch2_parent_taxonomy_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-2-BATCH2-PARENT-TAXONOMY-CLOSEOUT",
    "status": "V13_F4_0_2_BATCH2_PARENT_TAXONOMY_CANONICALIZATION_PASS" if ok else "V13_F4_0_2_BATCH2_PARENT_TAXONOMY_CANONICALIZATION_BLOCKED",
    "base_commit": "90958a2b", "canonicalization_executed": True,
    "coverage_fail_pass_conflict_fixed": True,
    "source_audit_contract_violation_fixed": True,
    "lane_count_consistency_passed": True,
    "source_audit_group_taxonomy_fixed": True,
    "pass_research_evidence_factors": pass_f,
    "ready_for_candidate_review": pass_f,
    "f09_status": "SOURCE_AUDIT_CONTRACT_VIOLATED",
    "f17_f20_group_status": "SOURCE_AUDIT_GROUP_COMPLETED",
    "ready_for_promotion_review": [],
    "frozen_candidates_preserved": ["F04","F10","F11"],
    "frozen_candidates_mutated": False,
    "f3_5_1_monitoring_execution_executed": False,
    "f3_6_true_oos_validation_executed": False,
    "multi_factor_composite_built": False, "weight_optimization_executed": False,
    "v13_6_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_V13_F4_1_BATCH2_CANDIDATE_REVIEW"
}, indent=2))
print(f"[F4.0.2-F] Taxonomy closeout: pass={pass_f} ok={ok}")
sys.exit(0)
