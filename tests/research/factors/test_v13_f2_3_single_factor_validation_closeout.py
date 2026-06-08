"""V13.F2.3 — Stage H: validation closeout tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

co = L("v13_f2_3_single_factor_validation_closeout.json")

def test_closeout_present():
    assert "V13_F2_3" in co.get("status", "")

def test_executed():
    assert co.get("v13_f2_3_executed") is True

def test_outcome_label_generated():
    assert co.get("outcome_label_generation_executed") is True

def test_label_isolation_checked():
    # May be True or False, but must be a boolean
    assert isinstance(co.get("label_isolation_passed"), bool)

def test_ic_executed():
    assert co.get("ic_validation_executed") is True

def test_rank_ic_executed():
    assert co.get("rank_ic_validation_executed") is True

def test_bucket_executed():
    assert co.get("bucket_return_validation_executed") is True

def test_regime_executed():
    assert co.get("regime_diagnostics_executed") is True

def test_cost_adjusted_executed():
    assert co.get("cost_adjusted_validation_executed") is True

def test_validated_factors():
    assert co.get("validated_factors") == ["F03", "F06"]

def test_per_factor_final_status_2():
    assert len(co.get("per_factor_final_status", [])) == 2

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

def test_next_action_populated():
    assert len(co.get("recommended_next_action", "")) > 0
