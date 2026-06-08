#!/usr/bin/env python3
"""V13.F3.0.1 — Stage B: audit all 8 child closeouts for evidence consistency."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

def load(fid, name):
    p = BATCH / fid / name
    return json.loads(p.read_text()) if p.exists() else {}

def recompute_evidence(fid):
    """Recompute evidence score from actual child artifacts, not closeout self-claim."""
    mat = load(fid, f"{fid.lower()}_materialization.json")
    pit = load(fid, f"{fid.lower()}_pit_leakage_validation.json")
    cov = load(fid, f"{fid.lower()}_coverage_validation.json")
    val = load(fid, f"{fid.lower()}_single_factor_validation.json")
    closeout = load(fid, f"{fid.lower()}_closeout.json")
    scorecard = load(fid, f"{fid.lower()}_evidence_scorecard.json")

    materialized = mat.get("materialization_executed", False) or mat.get("extended_panel_built", False)
    pit_pass = pit.get("pit_pass", False) if pit else False
    coverage_pass = cov.get("coverage_pass", False) if cov else False
    sample_count = max(mat.get("sample_month_count", 0), val.get("sample_month_count", 0))
    val_executed = val.get("single_factor_validation_executed", False)
    child_claimed = closeout.get("evidence_score", scorecard.get("evidence_score", "UNKNOWN"))

    reasons = []

    if closeout.get("planning_only"):
        return "HYPOTHESIS_ONLY", False, []

    if not materialized:
        return "NOT_MATERIALIZED", False, ["not_materialized"]

    if not pit_pass:
        return "PIT_BLOCKED", False, ["pit_failed"]

    if not coverage_pass:
        reasons.append(f"coverage_passed_false_but_child_claimed_{child_claimed}")
        if sample_count >= 12:
            return "MATERIALIZED_BUT_COVERAGE_BLOCKED", False, reasons
        else:
            return "BLOCKED_BY_SAMPLE_AND_COVERAGE", False, reasons

    if sample_count < 12:
        reasons.append(f"sample_month_count_{sample_count}_below_12")
        return "BLOCKED_BY_INSUFFICIENT_SAMPLE", False, reasons

    if not val_executed:
        reasons.append("single_factor_validation_not_executed")
        return "MATERIALIZED_BUT_VALIDATION_NOT_EXECUTED", False, reasons

    return "PASS_RESEARCH_EVIDENCE", True, []

inconsistent = []
coverage_fail_but_pass = []
pass_list = []
blocked_list = []
hypothesis_list = []

for fid in FACTOR_IDS:
    child_claimed = (load(fid, f"{fid.lower()}_closeout.json") or load(fid, f"{fid.lower()}_evidence_scorecard.json")).get("evidence_score", "UNKNOWN")
    recomputed, is_pass, reasons = recompute_evidence(fid)

    is_inconsistent = (is_pass and child_claimed != recomputed) or (not is_pass and child_claimed in ("PASS_RESEARCH_EVIDENCE", "TACTICAL_ONLY"))

    if fid in ("F04", "F10", "F11") and child_claimed == "PASS_RESEARCH_EVIDENCE" and not is_pass:
        coverage_fail_but_pass.append(fid)

    if is_inconsistent:
        inconsistent.append({
            "factor_id": fid,
            "child_claimed_evidence_score": child_claimed,
            "recomputed_evidence_score": recomputed,
            "claim_consistent_with_artifacts": False,
            "inconsistency_reasons": reasons
        })

    if is_pass:
        pass_list.append(fid)
    elif recomputed == "HYPOTHESIS_ONLY":
        hypothesis_list.append(fid)
    else:
        blocked_list.append(fid)

audit = {
    "pipeline_signature": "Z2-V13-F3-0-1-OPENCLAW-CHILD-AUDIT",
    "status": "V13_F3_0_CHILD_EVIDENCE_CONSISTENCY_AUDIT_BUILT",
    "audited_factor_count": 8,
    "inconsistent_factor_count": len(inconsistent),
    "inconsistent_factors": inconsistent,
    "coverage_fail_but_pass_claim_factors": coverage_fail_but_pass,
    "corrected_pass_research_evidence_factors": pass_list,
    "corrected_blocked_factors": blocked_list,
    "corrected_hypothesis_only_factors": hypothesis_list,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}

dst = BATCH / "v13_f3_0_child_evidence_consistency_audit.json"
dst.write_text(json.dumps(audit, indent=2))
print(f"[F3.0.1-B] Child consistency audit built -> {dst}")
print(f"  Inconsistent: {len(inconsistent)}")
for i in inconsistent:
    print(f"    ❌ {i['factor_id']}: claimed={i['child_claimed_evidence_score']} actual={i['recomputed_evidence_score']}")
print(f"  Corrected pass: {pass_list}")
print(f"  Corrected blocked: {blocked_list}")
print(f"  Hypothesis only: {hypothesis_list}")
sys.exit(0)
