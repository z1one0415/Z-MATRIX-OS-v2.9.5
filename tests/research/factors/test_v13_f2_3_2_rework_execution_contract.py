"""V13.F2.3.2 — Stage A: rework execution contract tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

c = L("v13_f2_3_2_rework_execution_contract.json")

def test_contract_built():
    assert c.get("status") == "V13_F2_3_2_REWORK_EXECUTION_CONTRACT_BUILT"

def test_primary_task():
    assert c.get("primary_task") == "F06_SAMPLE_EXTENSION"

def test_secondary_task():
    assert "F03R" in c.get("secondary_task", "")

def test_f06_extension_allowed():
    assert c.get("f06_sample_extension_allowed") is True

def test_f03r_planning_allowed():
    assert c.get("f03r_materialization_planning_allowed") is True

def test_f03r_not_materialized():
    assert c.get("f03r_materialization_executed") is False

def test_f03r_not_validated():
    assert c.get("f03r_validation_executed") is False

def test_ic_not_executed():
    assert c.get("ic_validation_executed") is False

def test_bucket_not_executed():
    assert c.get("bucket_return_validation_executed") is False

def test_multi_composite_false():
    assert c.get("multi_factor_composite_built") is False

def test_v13_6_false():
    assert c.get("v13_6_allowed") is False

def test_alpha_false():
    assert c.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert c.get("production") == "BLOCKED"
