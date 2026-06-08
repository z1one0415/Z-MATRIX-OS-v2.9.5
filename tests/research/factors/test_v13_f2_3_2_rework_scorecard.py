"""V13.F2.3.2 — Stage G: rework scorecard tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

sc = L("v13_f2_3_2_rework_scorecard.json")

def test_scorecard_built():
    assert sc.get("status") == "V13_F2_3_2_REWORK_SCORECARD_BUILT"

def test_f06_extension_attempted():
    assert sc.get("f06_extension_attempted") is True

def test_f06_ready_is_bool():
    assert isinstance(sc.get("f06_ready_for_revalidation"), bool)

def test_f06_sample_is_int():
    assert isinstance(sc.get("f06_sample_month_count_after_extension"), int)

def test_f03r_planning_built():
    assert sc.get("f03r_planning_built") is True

def test_f03r_not_materialized():
    assert sc.get("f03r_materialized") is False

def test_f03r_not_validated():
    assert sc.get("f03r_validated") is False

def test_ready_promotion_empty():
    assert sc.get("ready_for_promotion_review") == []

def test_multi_composite_false():
    assert sc.get("multi_factor_composite_built") is False

def test_oos_not_executed():
    assert sc.get("oos_alpha_validation_executed") is False

def test_v13_6_false():
    assert sc.get("v13_6_allowed") is False

def test_alpha_false():
    assert sc.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert sc.get("production") == "BLOCKED"
