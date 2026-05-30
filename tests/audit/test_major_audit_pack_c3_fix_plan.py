#!/usr/bin/env python3
"""Pack C.3: Blocking Risk Fix Plan Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_fix_plan_md_exists(): assert (WORKSPACE / "docs" / "audit" / "PACK_C3_BLOCKING_RISK_FIX_PLAN.md").exists()
def test_fix_plan_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").exists()
def test_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C3_CLOSEOUT.md").exists()

def test_exactly_2_risks():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").read_text())
    assert len(data) == 2

def test_risk_ids_correct():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").read_text())
    ids = {r["risk_id"] for r in data}
    assert ids == {"P1-001", "P1-004"}

def test_every_risk_has_fix_goal():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").read_text())
    for r in data: assert len(r["fix_goal"]) > 10

def test_every_risk_has_acceptance_criteria():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").read_text())
    for r in data: assert len(r["acceptance_criteria"]) >= 3

def test_account_truth_criteria_has_tolerance():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").read_text())
    at = next(r for r in data if r["risk_id"] == "P1-001")
    combined = " ".join(at["acceptance_criteria"])
    assert "tolerance" in combined.lower()
    assert "ERROR" in combined

def test_replay_criteria_has_calendar():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "pack_c3_blocking_risk_fix_plan.json").read_text())
    rp = next(r for r in data if r["risk_id"] == "P1-004")
    combined = " ".join(rp["acceptance_criteria"])
    assert "calendar" in combined.lower()
    assert "FAIL_CLOSED" in combined

def test_closeout_not_claim_fixed():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C3_CLOSEOUT.md").read_text()
    assert "FIXED" not in text or "NOT FIXED" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
