"""V13.F2.2 — Stage A: planning contract tests."""
import json
from pathlib import Path
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

c = L("v13_f2_2_single_factor_validation_planning_contract.json")

def test_planning_only():
    assert c.get("planning_only") is True

def test_validation_executed_false():
    assert c.get("validation_executed") is False

def test_ready_scope_f03():
    assert "F03" in c.get("validated_factor_scope", [])

def test_ready_scope_f06():
    assert "F06" in c.get("validated_factor_scope", [])

def test_ic_in_allowed():
    assert "IC" in c.get("allowed_validation_methods", [])

def test_rank_ic_in_allowed():
    assert "RANK_IC" in c.get("allowed_validation_methods", [])

def test_bucket_spread_in_allowed():
    assert "BUCKET_SPREAD" in c.get("allowed_validation_methods", [])

def test_horizon_split_in_allowed():
    assert "HORIZON_SPLIT" in c.get("allowed_validation_methods", [])

def test_regime_split_in_allowed():
    assert "REGIME_SPLIT" in c.get("allowed_validation_methods", [])

def test_cost_adjusted_in_allowed():
    assert "COST_ADJUSTED_SPREAD" in c.get("allowed_validation_methods", [])

def test_executed_empty():
    assert c.get("validation_methods_executed_this_round") == []

def test_multi_composite_false():
    assert c.get("multi_factor_composite_allowed") is False

def test_v13_6_false():
    assert c.get("v13_6_allowed") is False

def test_paper_trading_false():
    assert c.get("paper_trading_allowed") is False

def test_alpha_false():
    assert c.get("alpha_claim_allowed") is False

def test_production_blocked():
    assert c.get("production") == "BLOCKED"

def test_broker_blocked():
    assert c.get("broker_runtime") == "BLOCKED"

def test_real_trade_blocked():
    assert c.get("real_trade") == "BLOCKED"
