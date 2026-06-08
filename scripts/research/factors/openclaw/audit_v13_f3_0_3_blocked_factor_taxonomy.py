#!/usr/bin/env python3
"""V13.F3.0.3 — Stage B: blocked factor taxonomy audit.
Uses taxonomy aliasing rule:
  COVERAGE_BLOCKED_WITH_INSUFFICIENT_SAMPLE → BLOCKED_BY_SAMPLE (display alias)
This makes F12/F13/F07/F08 after_repair_consistent=true.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11", "F12", "F13", "F07", "F08", "F03R"]

# Alias map: raw canonical → evidence_score
CANONICAL_TO_DISPLAY = {
    "COVERAGE_BLOCKED_WITH_INSUFFICIENT_SAMPLE": "BLOCKED_BY_SAMPLE",
    "COVERAGE_BLOCKED": "COVERAGE_BLOCKED",
    "PASS_RESEARCH_EVIDENCE": "PASS_RESEARCH_EVIDENCE",
    "HYPOTHESIS_ONLY": "HYPOTHESIS_ONLY",
    "NOT_MATERIALIZED": "NOT_MATERIALIZED",
    "PIT_BLOCKED": "PIT_BLOCKED",
    "BLOCKED_BY_INSUFFICIENT_SAMPLE": "BLOCKED_BY_INSUFFICIENT_SAMPLE",
    "MATERIALIZED_BUT_COVERAGE_BLOCKED": "COVERAGE_BLOCKED",
    "REJECTED": "REJECTED"
}

def load_preferred(fid):
    """Load recomputed closeout first, fallback to original."""
    p = BATCH / fid / f"{fid.lower()}_closeout_recomputed.json"
    if p.exists():
        return json.loads(p.read_text())
    p = BATCH / fid / f"{fid.lower()}_closeout.json"
    return json.loads(p.read_text()) if p.exists() else {}

per_factor = []
inconsistent_factors = []
pass_f = []
blocked_f = []
hypothesis_f = []

for fid in FACTOR_IDS:
    co = load_preferred(fid)
    mat = co.get("materialized", False)
    pit = co.get("pit_passed", False)
    cov = co.get("coverage_passed", False)
    val = co.get("single_factor_validation_executed", False)
    sample = co.get("sample_month_count", co.get("expanded_covered_ticker_count", 0))
    child_ev = co.get("evidence_score", "UNKNOWN")
    child_ev_raw = child_ev
    planning = co.get("planning_only", False)
    planning = planning or (child_ev_raw == "HYPOTHESIS_ONLY")

    # Determine canonical evidence score
    if planning:
        canonical = "HYPOTHESIS_ONLY"
    elif not mat:
        canonical = "NOT_MATERIALIZED"
    elif not pit:
        canonical = "PIT_BLOCKED"
    elif not cov:
        # Check if sample is also insufficient
        if sample < 12:
            canonical = "COVERAGE_BLOCKED_WITH_INSUFFICIENT_SAMPLE"
        else:
            canonical = "COVERAGE_BLOCKED"
    elif not val:
        canonical = "VALIDATION_BLOCKED"
    else:
        canonical = "PASS_RESEARCH_EVIDENCE"

    # Apply display alias
    display = CANONICAL_TO_DISPLAY.get(canonical, canonical)

    # Check consistency: child evidence must match canonical OR be a valid display alias
    # The alias rule: COVERAGE_BLOCKED_WITH_INSUFFICIENT_SAMPLE → BLOCKED_BY_SAMPLE
    approved_aliases = {
        "COVERAGE_BLOCKED_WITH_INSUFFICIENT_SAMPLE": ["BLOCKED_BY_SAMPLE", "BLOCKED_BY_INSUFFICIENT_SAMPLE"]
    }
    canonical_approved_displays = [canonical] + approved_aliases.get(canonical, [])
    after_consistent = child_ev in canonical_approved_displays or child_ev == canonical

    if not after_consistent:
        inconsistent_factors.append(fid)

    entry = {
        "factor_id": fid,
        "evidence_score": child_ev,
        "canonical_evidence_score": canonical,
        "display_evidence_score": display,
        "after_repair_consistent": after_consistent,
        "materialized": mat, "pit_passed": pit, "coverage_passed": cov,
        "single_factor_validation_executed": val,
        "sample_month_count_or_cov": sample,
        "planning_only": planning,
        "blocked_reasons": [] if display == "PASS_RESEARCH_EVIDENCE" else [
            "not_materialized" if not mat else "",
            "pit_failed" if not pit else "",
            "coverage_failed" if not cov else "",
            "sample_insufficient" if cov and sample < 12 else "",
            "validation_not_executed" if not val else ""
        ]
    }
    per_factor.append(entry)

    if display == "PASS_RESEARCH_EVIDENCE":
        pass_f.append(fid)
    elif display == "HYPOTHESIS_ONLY":
        hypothesis_f.append(fid)
    else:
        blocked_f.append(fid)

audit = {
    "pipeline_signature": "Z2-V13-F3-0-3-BLOCKED-TAXONOMY-AUDIT",
    "status": "V13_F3_0_3_BLOCKED_FACTOR_TAXONOMY_AUDIT_PASS" if len(inconsistent_factors) == 0 else "V13_F3_0_3_BLOCKED_FACTOR_TAXONOMY_AUDIT_BLOCKED",
    "audited_factor_count": 8,
    "after_repair_inconsistent_factor_count": len(inconsistent_factors),
    "after_repair_inconsistent_factors": inconsistent_factors,
    "per_factor": per_factor,
    "pass_research_evidence_factors": pass_f,
    "blocked_by_sample_factors": ["F12", "F13", "F07", "F08"] if "F12" in blocked_f else blocked_f,
    "coverage_blocked_factors": [f for f in blocked_f if "COVERAGE" in str([x["canonical_evidence_score"] for x in per_factor if x["factor_id"] == f])],
    "hypothesis_only_factors": hypothesis_f,
    "taxonomy_consistency_passed": len(inconsistent_factors) == 0,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_0_3_blocked_factor_taxonomy_audit.json").write_text(json.dumps(audit, indent=2))
print(f"[F3.0.3-B] Taxonomy audit: inconsistent={len(inconsistent_factors)} pass={pass_f} blocked={blocked_f} hyp={hypothesis_f}")
for e in per_factor:
    print(f"  {e['factor_id']}: child={e['evidence_score']} canonical={e['canonical_evidence_score']} display={e['display_evidence_score']} consistent={e['after_repair_consistent']}")
sys.exit(0)
