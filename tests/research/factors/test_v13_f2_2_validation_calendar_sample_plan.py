"""V13.F2.2 — Stage D: calendar / sample sufficiency tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

p = L("v13_f2_2_validation_calendar_sample_plan.json")

def test_plan_built():
    assert p.get("status") == "V13_F2_2_VALIDATION_CALENDAR_SAMPLE_PLAN_BUILT"

def test_rebalance_frequency():
    assert p.get("rebalance_frequency") == "MONTHLY"

def test_minimum_month_count():
    assert p.get("minimum_month_count_required") == 12

def test_preferred_month_count():
    assert p.get("preferred_month_count_required") == 24

def test_minimum_cross_section():
    assert p.get("minimum_cross_section_ticker_count") == 100

def test_sample_not_checked():
    assert p.get("sample_sufficiency_checked_this_round") is False

def test_sample_check_allowed():
    assert p.get("sample_sufficiency_check_allowed_next_step") is True

def test_horizons_20d():
    assert "20D" in p.get("validation_horizons", [])

def test_horizons_60d():
    assert "60D" in p.get("validation_horizons", [])

def test_alpha_false():
    assert p.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert p.get("production") == "BLOCKED"
