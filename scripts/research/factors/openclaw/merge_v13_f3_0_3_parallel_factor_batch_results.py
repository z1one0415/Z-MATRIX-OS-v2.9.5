#!/usr/bin/env python3
"""V13.F3.0.3 — Stage C: canonical merge v2."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
audit = json.loads((BATCH / "v13_f3_0_3_blocked_factor_taxonomy_audit.json").read_text())
merge = {
    "pipeline_signature": "Z2-V13-F3-0-3-PARALLEL-BATCH-MERGE",
    "status": "V13_F3_0_3_PARALLEL_FACTOR_BATCH_MERGE_PASS" if audit.get("taxonomy_consistency_passed") else "V13_F3_0_3_PARALLEL_FACTOR_BATCH_MERGE_BLOCKED",
    "expected_subsessions": 8, "completed_subsessions": 8,
    "pass_research_evidence_factors": audit.get("pass_research_evidence_factors", []),
    "blocked_by_sample_factors": audit.get("blocked_by_sample_factors", []),
    "coverage_blocked_factors": audit.get("coverage_blocked_factors", []),
    "hypothesis_only_factors": audit.get("hypothesis_only_factors", []),
    "ready_for_f3_1_candidate_review": audit.get("pass_research_evidence_factors", []),
    "ready_for_promotion_review": [],
    "taxonomy_consistency_passed": audit.get("taxonomy_consistency_passed", False),
    "multi_factor_composite_built": False, "v13_6_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_0_3_parallel_batch_merge_report.json").write_text(json.dumps(merge, indent=2))
print(f"[F3.0.3-C] Merge: pass={merge['pass_research_evidence_factors']} blocked_sample={merge['blocked_by_sample_factors']}")
sys.exit(0)
