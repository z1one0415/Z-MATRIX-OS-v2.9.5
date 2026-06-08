"""V13.F2.3.1 — Stage G: evidence disposition closeout tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

co = L("v13_f2_3_1_evidence_disposition_closeout.json")

def test_closeout_pass():
    assert co.get("status") == "V13_F2_3_1_EVIDENCE_DISPOSITION_CLOSEOUT_PASS"

def test_executed():
    assert co.get("v13_f2_3_1_executed") is True

def test_f03_disposition():
    assert co.get("f03_disposition") == "REJECTED_CURRENT_DIRECTION"

def test_f03r_registered():
    assert co.get("f03r_hypothesis_registered") is True

def test_f03r_not_materialized():
    assert co.get("f03r_materialized") is False

def test_f03r_not_validated():
    assert co.get("f03r_validated") is False

def test_f06_disposition():
    assert co.get("f06_disposition") == "BLOCKED_BY_INSUFFICIENT_SAMPLE"

def test_f06_extension_plan_built():
    assert co.get("f06_sample_extension_plan_built") is True

def test_ready_for_promotion_empty():
    assert co.get("ready_for_f2_4_promotion_review") == []

def test_promotion_not_allowed():
    assert co.get("promotion_review_allowed") is False

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
