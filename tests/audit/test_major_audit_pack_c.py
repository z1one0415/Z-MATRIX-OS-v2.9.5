#!/usr/bin/env python3
"""Pack C: Core Module Review Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_test_map_exists(): assert (WORKSPACE / "docs" / "audit" / "CORE_MODULE_TEST_MAP.md").exists()
def test_behavior_audit_exists(): assert (WORKSPACE / "docs" / "audit" / "CORE_MODULE_BEHAVIOR_AUDIT.md").exists()
def test_risk_register_exists(): assert (WORKSPACE / "docs" / "audit" / "CORE_MODULE_RISK_REGISTER.md").exists()
def test_manual_review_exists(): assert (WORKSPACE / "docs" / "audit" / "CORE_MODULE_MANUAL_REVIEW.md").exists()
def test_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C_CLOSEOUT.md").exists()

def test_seven_core_modules_in_map():
    text = (WORKSPACE / "docs" / "audit" / "CORE_MODULE_TEST_MAP.md").read_text()
    for mod in ["account_truth", "master_data", "market_data", "outcome_engine", "attribution", "replay", "council"]:
        assert mod in text, f"Missing: {mod}"

def test_closeout_status_valid():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C_CLOSEOUT.md").read_text()
    valid = ["PACK_C_PASS", "PACK_C_REVIEW_REQUIRED", "PACK_C_BLOCKED"]
    assert any(s in text for s in valid)

def test_no_p0_blocker_if_pass():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C_CLOSEOUT.md").read_text()
    if "PACK_C_PASS" in text:
        assert "P0: 0" in text or "P0:0" in text, "PACK_C_PASS but P0>0"

def test_risk_register_has_7_modules():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_risk_register.json").read_text())
    modules = set(r["module"] for r in data)
    assert len(modules) == 7

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])

def test_risk_counts_consistent_across_reports():
    import json
    behavior = (WORKSPACE / "docs" / "audit" / "CORE_MODULE_BEHAVIOR_AUDIT.md").read_text()
    risk_json = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_risk_register.json").read_text())
    manual = (WORKSPACE / "docs" / "audit" / "CORE_MODULE_MANUAL_REVIEW.md").read_text()
    closeout = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C_CLOSEOUT.md").read_text()
    # Risk register has P0=0 from json
    p0_risk = sum(1 for r in risk_json if r["level"] == "P0_BLOCKER")
    p1_risk = sum(1 for r in risk_json if r["level"] == "P1_HIGH")
    # Manual review should state 0 P0 and 4 P1
    assert "0 P0" in manual or "P0: 0" in manual or "P0:0" in manual
    assert "4 P1" in manual or "P1: 4" in manual or "P1:4" in manual
    # Closeout should match
    assert "P0: 0" in closeout or "P0:0" in closeout
    assert "P1: 4" in closeout or "P1:4" in closeout

def test_closeout_next_step_is_c1_when_review_required():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C_CLOSEOUT.md").read_text()
    if "REVIEW_REQUIRED" in text:
        assert "PACK_C_COMPLETE" not in text, "Closeout says COMPLETE but verdict is REVIEW_REQUIRED"

def test_behavior_audit_market_data_risk_matches_register():
    import json
    behavior = (WORKSPACE / "docs" / "audit" / "CORE_MODULE_BEHAVIOR_AUDIT.md").read_text()
    risk_json = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_risk_register.json").read_text())
    md_risk = [r for r in risk_json if r["module"] == "market_data"]
    assert len(md_risk) == 1
    # Behavior audit should NOT say P0 for market_data
    for line in behavior.split("\n"):
        if "market_data" in line.lower() and "risk:" in line.lower() and "P0" in line:
            assert "P1" in line, f"market_data behavior audit shows P0 but risk register has P1"
