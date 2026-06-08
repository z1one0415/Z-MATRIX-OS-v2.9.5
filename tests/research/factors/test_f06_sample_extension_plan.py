"""V13.F2.3.1 — Stage E: F06 sample extension plan tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

p = L("f06_fundamental_quality_sample_extension_plan.json")

def test_plan_built():
    assert p.get("status") == "F06_SAMPLE_EXTENSION_PLAN_BUILT"

def test_factor_id():
    assert p.get("factor_id") == "F06"

def test_current_sample():
    assert p.get("current_sample_month_count") == 1

def test_minimum_required():
    assert p.get("minimum_month_count_required") == 12

def test_preferred_required():
    assert p.get("preferred_month_count_required") == 24

def test_minimum_additional():
    ext = p.get("required_extension_target", {})
    assert ext.get("minimum_additional_months_needed", 0) >= 11

def test_preferred_additional():
    ext = p.get("required_extension_target", {})
    assert ext.get("preferred_additional_months_needed", 0) >= 23

def test_expand_history_allowed():
    assert "EXPAND_FUNDAMENTAL_HISTORY" in p.get("extension_methods_allowed", [])

def test_synthetic_fundamentals_forbidden():
    assert "SYNTHETIC_FUNDAMENTALS" in p.get("extension_methods_forbidden", [])

def test_forward_fill_forbidden():
    assert "FORWARD_FILLED_FUTURE_STATEMENTS" in p.get("extension_methods_forbidden", [])

def test_lookahead_forbidden():
    assert "LOOKAHEAD_ANN_DATE" in p.get("extension_methods_forbidden", [])

def test_outcome_imputation_forbidden():
    assert "OUTCOME_LABEL_IMPUTATION" in p.get("extension_methods_forbidden", [])

def test_materialization_allowed():
    assert p.get("materialization_allowed_next_gate") is True

def test_validation_allowed():
    assert p.get("validation_allowed_after_extension") is True

def test_alpha_false():
    assert p.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert p.get("production") == "BLOCKED"
