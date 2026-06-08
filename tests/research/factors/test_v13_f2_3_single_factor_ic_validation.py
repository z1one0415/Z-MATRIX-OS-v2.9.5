"""V13.F2.3 — Stage D: IC validation tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

ic = L("v13_f2_3_single_factor_ic_validation.json")

def test_ic_validated():
    assert ic.get("ic_validation_executed") is True

def test_rank_ic_validated():
    assert ic.get("rank_ic_validation_executed") is True

def test_validated_factors():
    assert "F03" in ic.get("validated_factors", [])
    assert "F06" in ic.get("validated_factors", [])

def test_minimum_month_count():
    assert ic.get("minimum_month_count_required") == 12

def test_per_factor_ic_count():
    assert len(ic.get("per_factor_ic", [])) == 2

def test_f03_ic_executed():
    f03 = next((f for f in ic.get("per_factor_ic", []) if f["factor_id"] == "F03"), None)
    assert f03 is not None
    assert f03.get("ic_validation_executed") is True
    assert f03.get("sample_month_count", 0) >= 12

def test_f06_ic_executed():
    f06 = next((f for f in ic.get("per_factor_ic", []) if f["factor_id"] == "F06"), None)
    assert f06 is not None
    assert f06.get("ic_validation_executed") is True

def test_f03_has_ic_values():
    f03 = next((f for f in ic.get("per_factor_ic", []) if f["factor_id"] == "F03"), None)
    assert isinstance(f03.get("ic_20d_mean"), (int, float))
    assert isinstance(f03.get("ic_60d_mean"), (int, float))

def test_f03_has_win_rate():
    f03 = next((f for f in ic.get("per_factor_ic", []) if f["factor_id"] == "F03"), None)
    assert 0 <= f03.get("ic_20d_win_rate", -1) <= 1

def test_alpha_false():
    assert ic.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert ic.get("production") == "BLOCKED"
