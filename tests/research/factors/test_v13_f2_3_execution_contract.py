"""V13.F2.3 — Stage A: execution contract tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

c = L("v13_f2_3_single_factor_validation_execution_contract.json")

def test_contract_built():
    assert c.get("status") == "V13_F2_3_SINGLE_FACTOR_VALIDATION_EXECUTION_CONTRACT_BUILT"

def test_execution_scope():
    assert c.get("execution_scope") == ["F03", "F06"]

def test_validation_allowed():
    assert c.get("validation_execution_allowed") is True

def test_label_generation_allowed():
    assert c.get("outcome_label_generation_allowed") is True

def test_label_write_to_panel_not_allowed():
    assert c.get("outcome_label_write_to_factor_panel_allowed") is False

def test_ic_allowed():
    assert c.get("ic_validation_allowed") is True

def test_rank_ic_allowed():
    assert c.get("rank_ic_validation_allowed") is True

def test_bucket_allowed():
    assert c.get("bucket_return_validation_allowed") is True

def test_horizon_split_allowed():
    assert c.get("horizon_split_allowed") is True

def test_regime_split_allowed():
    assert c.get("regime_split_allowed") is True

def test_cost_adjusted_allowed():
    assert c.get("cost_adjusted_allowed") is True

def test_multi_composite_false():
    assert c.get("multi_factor_composite_allowed") is False

def test_v13_6_false():
    assert c.get("v13_6_allowed") is False

def test_paper_false():
    assert c.get("paper_trading_allowed") is False

def test_alpha_false():
    assert c.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert c.get("production") == "BLOCKED"
