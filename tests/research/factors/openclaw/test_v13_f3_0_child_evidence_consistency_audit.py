"""V13.F3.0.1 — Child evidence consistency audit tests."""
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"

def load(name):
    p = BATCH / name
    return json.loads(p.read_text()) if p.exists() else {}

a = load("v13_f3_0_child_evidence_consistency_audit.json")

def test_audit_built():
    assert "AUDIT" in a.get("status", "")

def test_audited_8():
    assert a.get("audited_factor_count") == 8

def test_f04_inconsistent_detected():
    for f in a.get("inconsistent_factors", []):
        if f["factor_id"] == "F04":
            assert f["claim_consistent_with_artifacts"] is False

def test_f10_inconsistent_detected():
    for f in a.get("inconsistent_factors", []):
        if f["factor_id"] == "F10":
            assert f["claim_consistent_with_artifacts"] is False

def test_f11_inconsistent_detected():
    for f in a.get("inconsistent_factors", []):
        if f["factor_id"] == "F11":
            assert f["claim_consistent_with_artifacts"] is False

def test_inconsistent_3():
    assert a.get("inconsistent_factor_count") == 3

def test_coverage_fail_pass_identified():
    assert "F04" in a.get("coverage_fail_but_pass_claim_factors", [])

def test_corrected_pass():
    assert isinstance(a.get("corrected_pass_research_evidence_factors"), list)

def test_corrected_blocked():
    assert isinstance(a.get("corrected_blocked_factors"), list)

def test_alpha_false():
    assert a.get("alpha_claim_allowed") is False
