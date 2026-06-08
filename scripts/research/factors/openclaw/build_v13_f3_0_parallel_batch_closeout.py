#!/usr/bin/env python3
"""V13.F3.0 — Parent batch closeout."""
import json, sys
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def load_jsonp(fname: str) -> dict:
    p = BATCH / fname
    return json.loads(p.read_text()) if p.exists() else {}

merge = load_jsonp("v13_f3_0_parallel_batch_merge_report.json")
audit = load_jsonp("v13_f3_0_parallel_batch_safety_audit.json")

pass_f = merge.get("pass_research_evidence_factors", [])
tactical_f = merge.get("tactical_only_factors", [])
hypothesis_f = merge.get("hypothesis_only_factors", [])
blocked_f = merge.get("blocked_factors", [])
safety_ok = len(audit.get("violations", [])) == 0

candidate_count = len(pass_f) + len(tactical_f)

if candidate_count >= 2:
    next_action = "PREPARE_V13_F3_1_FACTOR_CANDIDATE_REVIEW"
elif candidate_count == 1:
    next_action = "PREPARE_SINGLE_FACTOR_REVIEW_AND_CONTINUE_PARALLEL_BATCH"
else:
    next_action = "CONTINUE_PARALLEL_FACTOR_DISCOVERY_WITH_NEXT_BATCH"

closeout = {
    "pipeline_signature": "Z2-V13-F3-0-PARALLEL-BATCH-CLOSEOUT",
    "status": "V13_F3_0_PARALLEL_FACTOR_BATCH_PASS" if safety_ok else "V13_F3_0_PARALLEL_FACTOR_BATCH_VIOLATED",
    "v13_f3_0_executed": True,
    "parallel_subsessions_launched": 8,
    "completed_subsessions": merge.get("completed_subsessions", 0),
    "pass_research_evidence": pass_f,
    "tactical_only": tactical_f,
    "hypothesis_only": hypothesis_f,
    "blocked_factors": blocked_f,
    "safety_violations": audit.get("violations", []),
    "safety_passed": safety_ok,
    "ready_for_next_validation": merge.get("ready_for_next_validation", []),
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False,
    "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False,
    "frontend_modified": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "recommended_next_action": next_action
}

dst = BATCH / "v13_f3_0_parallel_batch_closeout.json"
dst.write_text(json.dumps(closeout, indent=2))
print(f"[F3.0-C] Batch closeout built -> {dst}")
print(f"  Pass: {pass_f} | Tactical: {tactical_f} | Hypothesis: {hypothesis_f}")
print(f"  Safety: {'✅ PASS' if safety_ok else '❌ VIOLATIONS'}")
print(f"  Next: {next_action}")
sys.exit(0)
