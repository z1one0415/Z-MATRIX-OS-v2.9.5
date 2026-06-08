#!/usr/bin/env python3
"""V13.F3.1 — Stage B: candidate evidence package builder."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04", "F10", "F11"]

def load_preferred(fid, name):
    for suffix in ["_closeout_recomputed.json", "_closeout.json"]:
        p = BATCH / fid / f"{fid.lower()}{suffix}"
        if p.exists():
            base = dict(json.loads(p.read_text()))
            break
    else:
        return {"factor_id": fid, "error": "closeout_not_found"}
    # Load supporting artifacts
    mat = json.loads((BATCH / fid / f"{fid.lower()}_materialization.json").read_text()) if (BATCH / fid / f"{fid.lower()}_materialization.json").exists() else {}
    pit = json.loads((BATCH / fid / f"{fid.lower()}_pit_leakage_validation.json").read_text()) if (BATCH / fid / f"{fid.lower()}_pit_leakage_validation.json").exists() else {}
    cov = json.loads((BATCH / fid / f"{fid.lower()}_coverage_validation.json").read_text()) if (BATCH / fid / f"{fid.lower()}_coverage_validation.json").exists() else {}
    val = json.loads((BATCH / fid / f"{fid.lower()}_single_factor_validation.json").read_text()) if (BATCH / fid / f"{fid.lower()}_single_factor_validation.json").exists() else {}
    fcon = json.loads((BATCH / fid / f"{fid.lower()}_formula_contract.json").read_text()) if (BATCH / fid / f"{fid.lower()}_formula_contract.json").exists() else {}
    # Check coverage expansion
    cov_exp = json.loads((BATCH / fid / f"{fid.lower()}_coverage_expansion_repair.json").read_text()) if (BATCH / fid / f"{fid.lower()}_coverage_expansion_repair.json").exists() else {}

    materialized = mat.get("materialization_executed", False) or mat.get("extended_panel_built", False)
    pit_pass = pit.get("pit_pass", False)
    cov_pass = cov_exp.get("coverage_passed", False) or cov.get("coverage_pass", False)
    cov_tier = cov_exp.get("coverage_tier", "N/A")
    cov_count = cov_exp.get("expanded_covered_ticker_count", cov.get("covered_ticker_count", 0))
    val_exec = val.get("single_factor_validation_executed", False)
    ic_exec = val.get("ic_validation_executed", False)
    sample = val.get("sample_month_count", 0)
    ev = base.get("evidence_score", "UNKNOWN")
    horizons = fcon.get("horizons", [])
    formula = fcon.get("formula", "")

    known_risks = []
    if not materialized: known_risks.append("NOT_MATERIALIZED")
    if not pit_pass: known_risks.append("PIT_FAIL")
    if not cov_pass: known_risks.append("COVERAGE_FAIL")
    if not val_exec: known_risks.append("VALIDATION_NOT_EXECUTED")
    if not ic_exec: known_risks.append("IC_NOT_EXECUTED")
    if sample < 12: known_risks.append("SAMPLE_INSUFFICIENT")

    research_only_flags = []
    source = mat.get("source", "")
    if "research_simulation" in str(mat).lower():
        research_only_flags.append("RESEARCH_SIMULATION")

    return {
        "factor_id": fid,
        "factor_name": fcon.get("factor_name", base.get("factor_name", "")),
        "formula": formula,
        "horizons": horizons,
        "evidence_score": ev,
        "materialized": materialized,
        "pit_passed": pit_pass,
        "coverage_passed": cov_pass,
        "coverage_tier": cov_tier,
        "covered_ticker_count": cov_count,
        "total_universe": cov.get("total_universe_tickers", 5523),
        "sample_month_count": sample,
        "single_factor_validation_executed": val_exec,
        "ic_executed": ic_exec,
        "ic_summary": {
            "mean_ic_20d": val.get("ic_20d_mean", "N/A"),
            "mean_ic_60d": val.get("ic_60d_mean", "N/A"),
            "evidence_score": val.get("evidence_score", "N/A")
        },
        "bucket_summary": {
            "high_low_spread_20d": "N/A",
            "high_low_spread_60d": "N/A",
            "cost_adjusted_20d": "N/A"
        },
        "known_risks": known_risks,
        "research_only_flags": research_only_flags,
        "alpha_claim_allowed": False, "production": "BLOCKED",
        "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    }

packages = [load_preferred(fid, "") for fid in FACTORS]
result = {
    "pipeline_signature": "Z2-V13-F3-1-CANDIDATE-EVIDENCE-PACKAGES",
    "status": "V13_F3_1_CANDIDATE_EVIDENCE_PACKAGES_BUILT",
    "candidate_review_factors": FACTORS,
    "evidence_packages": packages,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_1_candidate_evidence_packages.json").write_text(json.dumps(result, indent=2))
print(f"[F3.1-B] Evidence packages built for {FACTORS}")
sys.exit(0)
