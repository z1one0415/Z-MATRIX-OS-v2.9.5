"""V13.F2.3.1 — Stage A: disposition contract tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

c = L("v13_f2_3_1_evidence_disposition_contract.json")

def test_contract_built():
    assert c.get("status") == "V13_F2_3_1_EVIDENCE_DISPOSITION_CONTRACT_BUILT"

def test_disposition_only():
    assert c.get("disposition_only") is True

def test_materialization_not_executed():
    assert c.get("materialization_executed") is False

def test_validation_not_executed():
    assert c.get("validation_executed") is False

def test_multi_composite_false():
    assert c.get("multi_factor_composite_built") is False

def test_promotion_review_false():
    assert c.get("promotion_review_allowed") is False

def test_target_factors():
    assert c.get("target_factors") == ["F03", "F06"]

def test_new_hypothesis_registration_allowed():
    assert c.get("new_hypothesis_registration_allowed") is True

def test_new_hypothesis_validation_not_allowed():
    assert c.get("new_hypothesis_validation_allowed") is False

def test_v13_6_false():
    assert c.get("v13_6_allowed") is False

def test_paper_false():
    assert c.get("paper_trading_allowed") is False

def test_alpha_false():
    assert c.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert c.get("production") == "BLOCKED"
