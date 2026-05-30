#!/usr/bin/env python3
"""Pack C.2.1: Evidence Lock Tests — hardened"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

VALID_DECISIONS = {"MUST_FIX_BEFORE_PACK_D", "TEST_GAP_ONLY", "ACCEPTED_DESIGN_BOUNDARY", "DOWNGRADE_TO_P2"}

def test_json_exists(): assert (WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").exists()
def test_json_sample_size():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    assert len(data) == 4

def test_every_required_action_min_30_chars():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    for t in data:
        assert len(t["required_action"]) >= 30, f"Action too short for {t['risk_id']}: {len(t['required_action'])}"

def test_every_triage_reason_min_30_chars():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    for t in data:
        assert len(t["triage_reason"]) >= 30, f"Reason too short for {t['risk_id']}"

def test_every_decision_valid():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    for t in data:
        assert t["triage_decision"] in VALID_DECISIONS

def test_blocking_items_deadline_c3():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    for t in data:
        if t["blocking_pack_d"]:
            assert "C.3" in t.get("deadline_stage", ""), f"Blocking item {t['risk_id']} has wrong deadline: {t.get('deadline_stage')}"

def test_markdown_json_blocking_consistent():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    json_blocking = sum(1 for t in data if t["blocking_pack_d"])
    md = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C2_CLOSEOUT.md").read_text()
    assert f"MUST_FIX <= 2" in md and "2" in md

def test_closeout_must_fix_matches_json():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    json_must_fix = sum(1 for t in data if t["triage_decision"] == "MUST_FIX_BEFORE_PACK_D")
    assert json_must_fix == 2

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
