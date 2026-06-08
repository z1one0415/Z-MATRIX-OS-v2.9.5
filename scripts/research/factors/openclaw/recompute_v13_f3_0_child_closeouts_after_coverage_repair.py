#!/usr/bin/env python3
"""V13.F3.0.1 — Stage D: recompute child closeouts after coverage repair."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTOR_IDS = ["F04", "F10", "F11"]

def load(fid, name):
    p = BATCH / fid / name
    return json.loads(p.read_text()) if p.exists() else {}

def wj(fid, name, data):
    (BATCH / fid / name).write_text(json.dumps(data, indent=2))

for fid in FACTOR_IDS:
    mat = load(fid, f"{fid.lower()}_materialization.json")
    pit = load(fid, f"{fid.lower()}_pit_leakage_validation.json")
    cov_repair = load(fid, f"{fid.lower()}_coverage_expansion_repair.json")
    val = load(fid, f"{fid.lower()}_single_factor_validation.json")
    original_closeout = load(fid, f"{fid.lower()}_closeout.json")

    materialized = mat.get("materialization_executed", False) or mat.get("extended_panel_built", False)
    pit_pass = pit.get("pit_pass", False)
    coverage_pass = cov_repair.get("coverage_passed", False)
    sample_count = cov_repair.get("expanded_covered_ticker_count", 0)
    val_executed = val.get("single_factor_validation_executed", False)
    has_validation = val.get("ic_validation_executed", False)

    if not materialized:
        evidence = "NOT_MATERIALIZED"
        subsession_status = "BLOCKED"
    elif not pit_pass:
        evidence = "PIT_BLOCKED"
        subsession_status = "BLOCKED"
    elif not coverage_pass:
        evidence = "MATERIALIZED_BUT_COVERAGE_BLOCKED"
        subsession_status = "BLOCKED"
    elif not val_executed or not has_validation:
        evidence = "MATERIALIZED_BUT_VALIDATION_NOT_EXECUTED"
        subsession_status = "BLOCKED"
    else:
        evidence = "PASS_RESEARCH_EVIDENCE"
        subsession_status = "PASS"

    recomputed = {
        "pipeline_signature": "Z2-V13-F3-0-1-RECOMPUTED-CLOSEOUT",
        "factor_id": fid,
        "factor_name": original_closeout.get("factor_name", ""),
        "subsession_status": subsession_status,
        "materialized": materialized,
        "pit_passed": pit_pass,
        "coverage_passed": coverage_pass,
        "coverage_tier": cov_repair.get("coverage_tier", "UNKNOWN"),
        "expanded_covered_ticker_count": cov_repair.get("expanded_covered_ticker_count", 0),
        "single_factor_validation_executed": val_executed,
        "evidence_score": evidence,
        "recomputed_from_artifacts": True,
        "ready_for_parent_merge": True,
        "ready_for_next_validation": subsession_status == "PASS",
        "ready_for_promotion_review": False,
        "multi_factor_composite_built": False,
        "v13_6_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "repair_note": f"Original closeout claimed {original_closeout.get('evidence_score', 'UNKNOWN')} but artifacts show {evidence}"
    }
    wj(fid, f"{fid.lower()}_closeout_recomputed.json", recomputed)
    print(f"[{fid}] Recomputed: {evidence} (cov={coverage_pass}, pit={pit_pass}, val={val_executed})")

sys.exit(0)
