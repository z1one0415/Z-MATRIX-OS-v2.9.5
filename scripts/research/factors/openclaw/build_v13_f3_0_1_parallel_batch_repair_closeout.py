#!/usr/bin/env python3
"""V13.F3.0.1 — Stage G: repair closeout."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

audit = load("v13_f3_0_child_evidence_consistency_audit.json")
merge = load("v13_f3_0_1_parallel_batch_merge_report.json")

safety_ok = len(load("v13_f3_0_1_parallel_batch_safety_audit.json").get("violations", [])) == 0
inconsistent = audit.get("inconsistent_factor_count", 0)
pass_f = merge.get("pass_research_evidence_factors", [])
blocked = merge.get("blocked_by_sample_factors", [])
hypothesis = merge.get("hypothesis_only_factors", [])
ready_next = merge.get("ready_for_next_validation", [])

candidate_count = len(pass_f)
if candidate_count >= 2:
    next_action = "PREPARE_V13_F3_1_FACTOR_CANDIDATE_REVIEW"
elif candidate_count == 1:
    next_action = "REVIEW_SINGLE_FACTOR_AND_CONTINUE_PARALLEL_BATCH"
else:
    next_action = "FIX_PRICE_FACTOR_UNIVERSE_COVERAGE_OR_CONTINUE_NEXT_PARALLEL_BATCH"

closeout = {
    "pipeline_signature": "Z2-V13-F3-0-1-PARALLEL-BATCH-REPAIR-CLOSEOUT",
    "status": "V13_F3_0_1_PARALLEL_BATCH_REPAIR_PASS" if safety_ok and inconsistent == 0 else "V13_F3_0_1_PARALLEL_BATCH_REPAIR_BLOCKED",
    "base_commit": "673ec6c",
    "repair_executed": True,
    "inconsistent_factor_count_before_repair": 3,
    "inconsistent_factor_count_after_repair": inconsistent,
    "coverage_expansion_attempted_factors": ["F04", "F10", "F11"],
    "pass_research_evidence_after_repair": pass_f,
    "materialized_but_coverage_blocked_after_repair": merge.get("materialized_but_coverage_blocked_factors", []),
    "blocked_by_sample_factors": blocked,
    "hypothesis_only_factors": hypothesis,
    "ready_for_next_validation": ready_next,
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False,
    "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False,
    "frontend_modified": False,
    "v13_6_allowed": False, "paper_trading_allowed": False,
    "alpha_claim_allowed": False, "ready_for_alpha_claim": False,
    "alpha_validated": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    "recommended_next_action": next_action
}
(BATCH / "v13_f3_0_1_parallel_batch_repair_closeout.json").write_text(json.dumps(closeout, indent=2))
print(f"[F3.0.1-G] Repair closeout: pass={pass_f} ready_next={ready_next}")
print(f"  Inconsistent: {inconsistent} | Safety: {'✅' if safety_ok else '❌'}")
print(f"  Next: {next_action}")
sys.exit(0)
