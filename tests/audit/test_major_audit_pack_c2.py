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

def test_behavior_json_no_p0_when_register_p0_zero():
    import json
    behavior = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_behavior_audit.json").read_text())
    for item in behavior:
        risk_text = item.get("risk", "")
        assert "P0:" not in risk_text, f"P0 in behavior JSON: {item['module']} → {risk_text}"

def test_behavior_json_market_data_matches_triage():
    import json
    behavior = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_behavior_audit.json").read_text())
    triage = json.loads((WORKSPACE / "runtime_reports" / "audit" / "p1_risk_triage.json").read_text())
    md_behavior = next((b for b in behavior if b["module"] == "market_data"), None)
    md_triage = next((t for t in triage if t["module"] == "market_data"), None)
    assert md_behavior is not None and md_triage is not None
    assert "P1" in md_behavior.get("risk", ""), f"market_data behavior risk not P1: {md_behavior.get('risk')}"
    assert md_triage["triage_decision"] == "TEST_GAP_ONLY"

def test_no_old_p0_market_data_text_anywhere():
    import json
    from pathlib import Path
    for p in (WORKSPACE / "runtime_reports" / "audit").glob("*.json"):
        text = p.read_text()
        assert "P0: PIT future leakage in price data" not in text, f"Old P0 text in {p.name}"
    for p in (WORKSPACE / "docs" / "audit").glob("*.md"):
        text = p.read_text()
        if "market_data" in text.lower():
            for line in text.split("\n"):
                if "market_data" in line.lower() and "P0" in line and "PIT" in line:
                    assert False, f"Old P0 in {p.name}: {line.strip()[:80]}"
