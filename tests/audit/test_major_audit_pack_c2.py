#!/usr/bin/env python3
"""Pack C.2: P1 Risk Triage Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

VALID_DECISIONS = {"MUST_FIX_BEFORE_PACK_D", "TEST_GAP_ONLY", "ACCEPTED_DESIGN_BOUNDARY", "DOWNGRADE_TO_P2"}

def test_triage_table_exists(): assert (WORKSPACE / "docs" / "audit" / "P1_RISK_TRIAGE_TABLE.md").exists()
def test_triage_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").exists()
def test_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C2_CLOSEOUT.md").exists()

def test_all_4_p1_in_triage():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    assert len(data) == 4
    modules = {t["module"] for t in data}
    assert modules == {"account_truth", "market_data", "outcome_engine", "replay"}

def test_every_p1_has_decision():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    for t in data:
        assert t["triage_decision"] in VALID_DECISIONS, f"Invalid: {t['triage_decision']}"

def test_blocking_has_required_action():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    for t in data:
        if t["blocking_pack_d"]:
            assert t["required_action"], f"No action for blocking risk: {t['risk_id']}"

def test_closeout_verdict_valid():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C2_CLOSEOUT.md").read_text()
    assert "PACK_C2_PASS" in text or "PACK_C2_BLOCKED" in text

def test_closeout_not_pack_d_ready_unless_pass():
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C2_CLOSEOUT.md").read_text()
    if "PACK_C2_BLOCKED" in text:
        assert "PACK_D" not in text or "not" in text.lower()

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
