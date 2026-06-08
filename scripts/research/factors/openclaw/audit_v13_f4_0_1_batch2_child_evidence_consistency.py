#!/usr/bin/env python3
"""V13.F4.0.1 — Stage C: child evidence consistency audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
MAT_FACTORS = ["F02","F05","F14","F15","F16"]
CONTRACT_VIOLATED = ["F09"]

def load(fid, name):
    p = B2 / fid / name
    return json.loads(p.read_text()) if p.exists() else {}

results = []
inconsistent_factors = []

for fid in MAT_FACTORS + CONTRACT_VIOLATED:
    co = load(fid, f"{fid.lower()}_closeout.json")
    cov = load(fid, f"{fid.lower()}_coverage_validation.json")
    child_ev = co.get("evidence_score", "UNKNOWN")
    cov_pass = cov.get("coverage_pass", False)
    cov_count = cov.get("covered_ticker_count", 0)

    if fid in CONTRACT_VIOLATED:
        recomputed = "SOURCE_AUDIT_CONTRACT_VIOLATED"
        ready = False
        reasons = ["source_audit_only_lane_materialized_and_validated"]
        inconsistent = True
    elif not cov_pass:
        recomputed = "MATERIALIZED_BUT_COVERAGE_BLOCKED"
        ready = False
        reasons = [f"coverage_passed_false_but_child_claimed_{child_ev}"]
        inconsistent = True
    else:
        recomputed = child_ev
        ready = True
        reasons = []
        inconsistent = False

    if inconsistent:
        inconsistent_factors.append(fid)
    results.append({
        "factor_id": fid,
        "child_claimed_evidence_score": child_ev,
        "coverage_passed": cov_pass,
        "covered_ticker_count": cov_count,
        "recomputed_evidence_score": recomputed,
        "claim_consistent_with_artifacts": not inconsistent,
        "inconsistency_reasons": reasons,
        "ready_for_candidate_review": ready
    })

(B2 / "v13_f4_0_1_batch2_child_evidence_consistency_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-1-BATCH2-CHILD-EVIDENCE-CONSISTENCY-AUDIT",
    "status": "V13_F4_0_1_BATCH2_CHILD_EVIDENCE_CONSISTENCY_AUDIT_BUILT",
    "audited_factor_count": len(results),
    "inconsistent_factor_count": len(inconsistent_factors),
    "inconsistent_factors": inconsistent_factors,
    "per_factor": results,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0.1-C] Child audit: {len(inconsistent_factors)} inconsistent: {inconsistent_factors}")
sys.exit(0)
