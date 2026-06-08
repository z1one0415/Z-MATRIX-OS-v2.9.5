"""V13.F2.3.2 — Stage F: F03R materialization planning tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

pl = L("f03r_materialization_planning_contract.json")

def test_planning_built():
    assert pl.get("status") == "F03R_MATERIALIZATION_PLANNING_CONTRACT_BUILT"

def test_hypothesis_id():
    assert pl.get("hypothesis_id") == "F03R"

def test_parent_factor():
    assert pl.get("parent_factor_id") == "F03"

def test_planning_only():
    assert pl.get("planning_only") is True

def test_not_materialized():
    assert pl.get("materialization_executed") is False

def test_not_validated():
    assert pl.get("validation_executed") is False

def test_data_snooping_acknowledged():
    assert pl.get("data_snooping_risk_acknowledged") is True

def test_same_sample_forbidden():
    assert pl.get("same_sample_validation_for_promotion_forbidden") is True

def test_requires_holdout():
    assert pl.get("requires_separate_holdout_or_future_oos_validation") is True

def test_promotion_not_allowed():
    assert pl.get("promotion_review_allowed") is False

def test_alpha_false():
    assert pl.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert pl.get("production") == "BLOCKED"
