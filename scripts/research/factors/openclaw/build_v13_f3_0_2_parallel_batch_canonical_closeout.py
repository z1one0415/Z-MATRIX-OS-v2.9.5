#!/usr/bin/env python3
"""V13.F3.0.2 — Stage E: canonical closeout."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"

audit = json.loads((BATCH / "v13_f3_0_2_child_evidence_after_repair_audit.json").read_text())
merge = json.loads((BATCH / "v13_f3_0_2_parallel_batch_merge_report.json").read_text())
safety = json.loads((BATCH / "v13_f3_0_2_parallel_batch_safety_audit.json").read_text())

inconsistent_after = audit.get("after_repair_inconsistent_factor_count", 999)
safety_ok = safety.get("violation_count", 999) == 0
pass_f = merge.get("pass_research_evidence_factors", [])
ready_next = merge.get("ready_for_next_validation", [])
hypothesis_f = merge.get("hypothesis_only_factors", [])
blocked_f = merge.get("blocked_by_sample_factors", [])

all_ok = inconsistent_after == 0 and safety_ok

status = "V13_F3_0_2_PARALLEL_BATCH_CANONICAL_PASS" if all_ok else "V13_F3_0_2_PARALLEL_BATCH_CANONICAL_BLOCKED"
next_action = "PREPARE_V13_F3_1_FACTOR_CANDIDATE_REVIEW" if all_ok and len(pass_f) >= 2 else \
              "REVIEW_SINGLE_FACTOR" if all_ok and len(pass_f) == 1 else \
              "FIX_REMAINING_PARENT_MERGE_CONSISTENCY"

closeout = {
    "pipeline_signature": "Z2-V13-F3-0-2-PARALLEL-BATCH-CANONICAL-CLOSEOUT",
    "status": status, "base_commit": "6b80553",
    "canonicalization_executed": True,
    "materialization_rerun_executed": False, "single_factor_validation_rerun_executed": False,
    "inconsistent_factor_count_before_repair": 3,
    "inconsistent_factor_count_after_repair": inconsistent_after,
    "pass_research_evidence_after_repair": pass_f,
    "blocked_by_sample_factors": blocked_f,
    "hypothesis_only_factors": hypothesis_f,
    "ready_for_next_validation": ready_next,
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False, "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False, "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False,
    "alpha_validated": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": next_action
}
(BATCH / "v13_f3_0_2_parallel_batch_canonical_closeout.json").write_text(json.dumps(closeout, indent=2))
print(f"[F3.0.2-E] Canonical closeout: status={status}")
print(f"  Inconsistent after: {inconsistent_after} | Safety: {'✅' if safety_ok else '❌'}")
print(f"  Pass: {pass_f} | Ready: {ready_next} | Next: {next_action}")
sys.exit(0)
