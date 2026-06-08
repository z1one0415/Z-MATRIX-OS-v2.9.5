"""V13.F2.3.1 — Stage C: F03R hypothesis registry tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

r = L("f03r_industry_relative_reversal_hypothesis_registry.json")

def test_hypothesis_registered():
    assert r.get("status") == "F03R_INDUSTRY_RELATIVE_REVERSAL_HYPOTHESIS_REGISTERED"

def test_hypothesis_id():
    assert r.get("hypothesis_id") == "F03R"

def test_parent_factor():
    assert r.get("parent_factor_id") == "F03"

def test_parent_rejected():
    assert r.get("parent_factor_status") == "REJECTED_CURRENT_DIRECTION"

def test_hypothesis_type():
    assert r.get("hypothesis_type") == "DIRECTIONAL_REVERSAL_CANDIDATE"

def test_registration_only():
    assert r.get("registration_only") is True

def test_not_materialized():
    assert r.get("materialization_executed") is False

def test_not_validated():
    assert r.get("validation_executed") is False

def test_promotion_not_allowed():
    assert r.get("promotion_review_allowed") is False

def test_requires_separate_gate():
    assert r.get("requires_separate_materialization_gate") is True
    assert r.get("requires_separate_validation_gate") is True

def test_has_formula():
    assert "reversal" in r.get("proposed_formula", "").lower()

def test_has_economic_hypothesis():
    assert len(r.get("economic_hypothesis", "")) > 0

def test_alpha_false():
    assert r.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert r.get("production") == "BLOCKED"
