#!/usr/bin/env python3
"""V13.F3.0.3 — Stage E: taxonomy closeout."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
audit = json.loads((BATCH / "v13_f3_0_3_blocked_factor_taxonomy_audit.json").read_text())
merge = json.loads((BATCH / "v13_f3_0_3_parallel_batch_merge_report.json").read_text())
safety = json.loads((BATCH / "v13_f3_0_3_parallel_batch_safety_audit.json").read_text())
inconsistent = audit.get("after_repair_inconsistent_factor_count", 999)
safety_ok = safety.get("violation_count", 999) == 0
all_ok = inconsistent == 0 and safety_ok
status = "V13_F3_0_3_PARALLEL_BATCH_TAXONOMY_PASS" if all_ok else "V13_F3_0_3_PARALLEL_BATCH_TAXONOMY_BLOCKED"
pass_f = merge.get("pass_research_evidence_factors", [])
(BATCH / "v13_f3_0_3_parallel_batch_taxonomy_closeout.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-0-3-PARALLEL-BATCH-TAXONOMY-CLOSEOUT",
    "status": status, "base_commit": "8808fea",
    "taxonomy_canonicalization_executed": True,
    "materialization_rerun_executed": False, "single_factor_validation_rerun_executed": False,
    "after_repair_inconsistent_factor_count": inconsistent,
    "pass_research_evidence_factors": pass_f,
    "blocked_by_sample_factors": merge.get("blocked_by_sample_factors", []),
    "hypothesis_only_factors": merge.get("hypothesis_only_factors", []),
    "ready_for_f3_1_candidate_review": pass_f,
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False, "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False,
    "alpha_validated": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_V13_F3_1_FACTOR_CANDIDATE_REVIEW" if all_ok else "FIX_REMAINING_TAXONOMY"
}, indent=2))
print(f"[F3.0.3-E] Closeout: status={status} pass={pass_f} inconsistent={inconsistent}")
sys.exit(0)
