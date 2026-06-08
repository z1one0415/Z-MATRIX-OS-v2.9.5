#!/usr/bin/env python3
"""V13.F3.2 — Stage C: evidence provenance freeze audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04", "F10", "F11"]

def load_json(fid, name):
    p = BATCH / fid / name
    return json.loads(p.read_text()) if p.exists() else {}

results = []
all_u475 = True
all_pit = True
all_val = True
all_sources_valid = True

for fid in FACTORS:
    mat = load_json(fid, f"{fid.lower()}_materialization.json")
    pit = load_json(fid, f"{fid.lower()}_pit_leakage_validation.json")
    cov_exp = load_json(fid, f"{fid.lower()}_coverage_expansion_repair.json")
    val = load_json(fid, f"{fid.lower()}_single_factor_validation.json")
    scorecard = load_json(fid, f"{fid.lower()}_evidence_scorecard.json")
    co = load_json(fid, f"{fid.lower()}_closeout_recomputed.json") or load_json(fid, f"{fid.lower()}_closeout.json")

    cov_pass = cov_exp.get("coverage_passed", False)
    cov_tier = cov_exp.get("coverage_tier", "N/A")
    pit_pass = pit.get("pit_pass", False)
    val_exec = val.get("single_factor_validation_executed", False)
    alpha_ok = co.get("alpha_claim_allowed") is False if co else True
    prod_ok = co.get("production") == "BLOCKED" if co else True

    if not cov_pass or cov_tier != "U475": all_u475 = False
    if not pit_pass: all_pit = False
    if not val_exec: all_val = False
    if not alpha_ok or not prod_ok: all_sources_valid = False

    results.append({
        "factor_id": fid,
        "coverage_u475": cov_pass and cov_tier == "U475",
        "pit_passed": pit_pass,
        "single_factor_validation_executed": val_exec,
        "alpha_blocked": alpha_ok,
        "production_blocked": prod_ok,
        "source_valid": cov_pass and pit_pass and val_exec and alpha_ok and prod_ok
    })

blocked = [r for r in results if not r["source_valid"]]
audit = {
    "pipeline_signature": "Z2-V13-F3-2-CANDIDATE-FREEZE-EVIDENCE-PROVENANCE-AUDIT",
    "status": "V13_F3_2_CANDIDATE_FREEZE_EVIDENCE_PROVENANCE_AUDIT_PASS" if len(blocked) == 0 else "V13_F3_2_CANDIDATE_FREEZE_EVIDENCE_PROVENANCE_AUDIT_BLOCKED",
    "audited_factors": FACTORS,
    "all_candidate_sources_valid": len(blocked) == 0,
    "all_coverage_u475": all_u475,
    "all_pit_passed": all_pit,
    "all_single_factor_validation_executed": all_val,
    "provenance_passed_factor_count": len([r for r in results if r["source_valid"]]),
    "provenance_blocked_factor_count": len(blocked),
    "blocked_reasons": [r["factor_id"] for r in blocked],
    "per_factor": results,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}
(BATCH / "v13_f3_2_candidate_freeze_evidence_provenance_audit.json").write_text(json.dumps(audit, indent=2))
print(f"[F3.2-C] Provenance audit: {len(blocked)} blocked, {len([r for r in results if r['source_valid']])} valid")
sys.exit(0)
