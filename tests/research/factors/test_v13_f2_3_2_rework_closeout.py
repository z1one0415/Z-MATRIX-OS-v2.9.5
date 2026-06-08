"""V13.F2.3.2 — Stage H: rework closeout tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

co = L("v13_f2_3_2_rework_closeout.json")

def test_closeout_present():
    assert "V13_F2_3_2" in co.get("status", "")

def test_executed():
    assert co.get("v13_f2_3_2_executed") is True

def test_f06_extended():
    assert co.get("f06_sample_extension_executed") is True

def test_f06_ready_is_bool():
    assert isinstance(co.get("f06_ready_for_revalidation"), bool)

def test_f06_sample_is_int():
    assert isinstance(co.get("f06_sample_month_count_after_extension"), int)

def test_f03r_planning_built():
    assert co.get("f03r_materialization_planning_built") is True

def test_f03r_not_materialized():
    assert co.get("f03r_materialized") is False

def test_f03r_not_validated():
    assert co.get("f03r_validated") is False

def test_ready_validation_is_list():
    assert isinstance(co.get("ready_for_next_validation"), list)

def test_ready_promotion_empty():
    assert co.get("ready_for_promotion_review") == []

def test_multi_composite_false():
    assert co.get("multi_factor_composite_built") is False

def test_oos_not_executed():
    assert co.get("oos_alpha_validation_executed") is False

def test_skillos_unchanged():
    assert co.get("skillos_protocol_modified") is False

def test_frontend_unchanged():
    assert co.get("frontend_modified") is False

def test_v13_6_false():
    assert co.get("v13_6_allowed") is False

def test_paper_false():
    assert co.get("paper_trading_allowed") is False

def test_alpha_false():
    assert co.get("alpha_claim_allowed") is False

def test_ready_for_alpha_false():
    assert co.get("ready_for_alpha_claim") is False

def test_alpha_validated_false():
    assert co.get("alpha_validated") is False

def test_prod_blocked():
    assert co.get("production") == "BLOCKED"

def test_broker_blocked():
    assert co.get("broker_runtime") == "BLOCKED"

def test_real_trade_blocked():
    assert co.get("real_trade") == "BLOCKED"

def test_next_action():
    assert len(co.get("recommended_next_action", "")) > 0
