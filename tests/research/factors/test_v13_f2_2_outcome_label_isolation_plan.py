"""V13.F2.2 — Stage C: outcome label isolation tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

p = L("v13_f2_2_outcome_label_isolation_plan.json")

def test_plan_built():
    assert p.get("status") == "V13_F2_2_OUTCOME_LABEL_ISOLATION_PLAN_BUILT"

def test_label_generation_not_executed():
    assert p.get("label_generation_executed") is False

def test_label_generation_allowed():
    assert p.get("label_generation_allowed_next_step") is True

def test_label_role():
    assert p.get("label_role") == "OUTCOME_LABEL_ONLY"

def test_horizons_20d():
    assert "20D" in p.get("label_horizons", [])

def test_horizons_60d():
    assert "60D" in p.get("label_horizons", [])

def test_feature_panel_write_not_allowed():
    assert p.get("feature_panel_write_allowed") is False

def test_feature_panel_contains_labels_false():
    assert p.get("feature_panel_contains_outcome_labels") is False

def test_forbidden_in_factor_panels():
    forbidden = p.get("forbidden_in_factor_panels", [])
    assert "forward_return_20d" in forbidden
    assert "forward_return_60d" in forbidden
    assert "future_return" in forbidden
    assert "target_return" in forbidden
    assert "label" in forbidden

def test_required_label_columns():
    cols = p.get("required_label_columns", [])
    assert "rebalance_date" in cols
    assert "ticker" in cols
    assert "forward_return_20d" in cols
    assert "forward_return_60d" in cols
    assert "label_role" in cols

def test_alpha_false():
    assert p.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert p.get("production") == "BLOCKED"

def test_broker_blocked():
    assert p.get("broker_runtime") == "BLOCKED"

def test_real_trade_blocked():
    assert p.get("real_trade") == "BLOCKED"
