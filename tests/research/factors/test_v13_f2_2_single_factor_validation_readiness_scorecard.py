"""V13.F2.2 — Stage F: readiness scorecard tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

sc = L("v13_f2_2_single_factor_validation_readiness_scorecard.json")

def test_scorecard_built():
    assert sc.get("status") == "V13_F2_2_SINGLE_FACTOR_VALIDATION_READINESS_SCORECARD_BUILT"

def test_ready_count_2():
    assert sc.get("ready_factor_count") == 2

def test_ready_factors():
    assert sc.get("ready_factors") == ["F03", "F06"]

def test_blocked_count_0():
    assert sc.get("blocked_factor_count") == 0

def test_blocked_factors_empty():
    assert sc.get("blocked_factors") == []

def test_planning_complete():
    assert sc.get("validation_planning_complete") is True

def test_outcome_label_planned():
    assert sc.get("outcome_label_isolation_planned") is True

def test_calendar_planned():
    assert sc.get("calendar_sample_plan_built") is True

def test_diagnostic_planned():
    assert sc.get("factor_specific_diagnostic_plan_built") is True

def test_ready_f2_3():
    assert sc.get("ready_for_f2_3_single_factor_validation_execution") == ["F03", "F06"]

def test_validation_not_executed():
    assert sc.get("validation_executed") is False

def test_multi_composite_false():
    assert sc.get("multi_factor_composite_built") is False

def test_v13_6_false():
    assert sc.get("v13_6_allowed") is False

def test_paper_false():
    assert sc.get("paper_trading_allowed") is False

def test_alpha_false():
    assert sc.get("alpha_claim_allowed") is False

def test_ready_for_alpha_false():
    assert sc.get("ready_for_alpha_claim") is False

def test_alpha_validated_false():
    assert sc.get("alpha_validated") is False

def test_prod_blocked():
    assert sc.get("production") == "BLOCKED"

def test_broker_blocked():
    assert sc.get("broker_runtime") == "BLOCKED"

def test_real_trade_blocked():
    assert sc.get("real_trade") == "BLOCKED"
