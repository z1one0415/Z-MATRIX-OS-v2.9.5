"""V13.F2.2 — Stage G: planning closeout tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

co = L("v13_f2_2_single_factor_validation_planning_closeout.json")

def test_closeout_pass():
    assert co.get("status") == "V13_F2_2_SINGLE_FACTOR_VALIDATION_PLANNING_PASS"

def test_executed():
    assert co.get("v13_f2_2_executed") is True

def test_planning_only():
    assert co.get("planning_only") is True

def test_validation_not_executed():
    assert co.get("validation_executed") is False

def test_ready_for_f2_3():
    assert co.get("ready_for_f2_3_single_factor_validation_execution") == ["F03", "F06"]

def test_ic_not_executed():
    assert co.get("ic_validation_executed") is False

def test_rank_ic_not_executed():
    assert co.get("rank_ic_validation_executed") is False

def test_bucket_not_executed():
    assert co.get("bucket_return_validation_executed") is False

def test_outcome_not_executed():
    assert co.get("outcome_label_generation_executed") is False

def test_oos_not_executed():
    assert co.get("oos_alpha_validation_executed") is False

def test_multi_composite_false():
    assert co.get("multi_factor_composite_built") is False

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
