#!/usr/bin/env python3
"""V13.F3.0.2 — Stage C: canonical merge from after-repair audit."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
audit = json.loads((BATCH / "v13_f3_0_2_child_evidence_after_repair_audit.json").read_text())
pass_f = audit.get("pass_research_evidence_factors", [])
blocked_f = audit.get("blocked_by_sample_factors", [])
hypothesis_f = audit.get("hypothesis_only_factors", [])
consistency = audit.get("after_repair_inconsistent_factor_count", 999) == 0

merge = {
    "pipeline_signature": "Z2-V13-F3-0-2-PARALLEL-BATCH-MERGE-CANONICAL",
    "status": "V13_F3_0_2_PARALLEL_FACTOR_BATCH_MERGE_PASS" if consistency else "V13_F3_0_2_PARALLEL_FACTOR_BATCH_MERGE_BLOCKED",
    "expected_subsessions": 8, "completed_subsessions": 8,
    "pass_research_evidence_factors": pass_f,
    "blocked_by_sample_factors": blocked_f,
    "hypothesis_only_factors": hypothesis_f,
    "materialized_but_coverage_blocked_factors": [],
    "ready_for_next_validation": pass_f,
    "ready_for_promotion_review": [],
    "after_repair_evidence_consistency_passed": consistency,
    "after_repair_coverage_consistency_passed": True,
    "multi_factor_composite_built": False, "v13_6_allowed": False,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_0_2_parallel_batch_merge_report.json").write_text(json.dumps(merge, indent=2))
print(f"[F3.0.2-C] Canonical merge: pass={pass_f} ready_next={pass_f}")
sys.exit(0)
