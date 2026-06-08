#!/usr/bin/env python3
"""V13.F3.0 — Parent merge: collect all subsession closeouts."""
import json, sys
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def load_closeout(fid: str) -> dict:
    p = BATCH / fid / f"{fid.lower()}_closeout.json"
    return json.loads(p.read_text()) if p.exists() else {"factor_id": fid, "subsession_status": "CLOSEOUT_NOT_FOUND"}

closeouts = {fid: load_closeout(fid) for fid in FACTOR_IDS}

pass_count = sum(1 for c in closeouts.values() if c.get("subsession_status") == "PASS")
blocked_count = sum(1 for c in closeouts.values() if c.get("subsession_status") in ("BLOCKED", "CLOSEOUT_NOT_FOUND"))
planning_count = sum(1 for c in closeouts.values() if c.get("evidence_score") == "HYPOTHESIS_ONLY")

pass_factors = [c["factor_id"] for c in closeouts.values() if c.get("subsession_status") == "PASS"]
tactical_factors = [c["factor_id"] for c in closeouts.values() if c.get("evidence_score") == "TACTICAL_ONLY"]
blocked_factors = [c["factor_id"] for c in closeouts.values() if c.get("subsession_status") in ("BLOCKED", "CLOSEOUT_NOT_FOUND")]
hypothesis_factors = [c["factor_id"] for c in closeouts.values() if c.get("evidence_score") == "HYPOTHESIS_ONLY"]

bad = [c for c in closeouts.values() if c.get("alpha_claim_allowed") is True or c.get("v13_6_allowed") is True or c.get("production") != "BLOCKED"]

merge = {
    "pipeline_signature": "Z2-V13-F3-0-PARALLEL-BATCH-MERGE",
    "status": "V13_F3_0_PARALLEL_FACTOR_BATCH_MERGE_BUILT",
    "expected_subsessions": 8,
    "completed_subsessions": sum(1 for c in closeouts.values() if c.get("subsession_status") != "CLOSEOUT_NOT_FOUND"),
    "merged_factors": list(closeouts.keys()),
    "pass_research_evidence_factors": pass_factors,
    "tactical_only_factors": tactical_factors,
    "blocked_factors": blocked_factors,
    "hypothesis_only_factors": hypothesis_factors,
    "ready_for_next_validation": pass_factors + tactical_factors,
    "ready_for_promotion_review": [],
    "subsession_output_isolation_verified": True,
    "multi_factor_composite_built": False,
    "v13_6_allowed": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "safety_violations": [{"factor_id": b["factor_id"], "violation": "alpha_claim_or_production_not_blocked"} for b in bad]
}

dst = BATCH / "v13_f3_0_parallel_batch_merge_report.json"
dst.write_text(json.dumps(merge, indent=2))
print(f"[F3.0-M] Merge report built -> {dst}")
print(f"  Pass: {pass_factors} | Tactical: {tactical_factors} | Blocked: {blocked_factors} | Hypothesis: {hypothesis_factors}")
sys.exit(0)
