"""V13.F2.2 — Stage B: validation method contracts tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

mc = L("single_factor_validation_method_contracts.json")

def test_status():
    assert mc.get("status") == "SINGLE_FACTOR_VALIDATION_METHOD_CONTRACTS_BUILT"

def test_two_factors():
    assert mc.get("factor_count") == 2

def test_f03_present():
    ids = [f["factor_id"] for f in mc.get("factors", [])]
    assert "F03" in ids

def test_f06_present():
    ids = [f["factor_id"] for f in mc.get("factors", [])]
    assert "F06" in ids

def test_f03_validation_ready():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert f03["validation_ready"] is True

def test_f06_validation_ready():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert f06["validation_ready"] is True

def test_f03_ic_planned():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert f03["validation_methods"]["ic"]["enabled_next_step"] is True

def test_f06_ic_planned():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert f06["validation_methods"]["ic"]["enabled_next_step"] is True

def test_f03_rank_ic_planned():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert f03["validation_methods"]["rank_ic"]["enabled_next_step"] is True

def test_f06_rank_ic_planned():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert f06["validation_methods"]["rank_ic"]["enabled_next_step"] is True

def test_f03_bucket_3():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert f03["validation_methods"]["bucket_spread"]["bucket_count"] == 3

def test_f06_bucket_3():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert f06["validation_methods"]["bucket_spread"]["bucket_count"] == 3

def test_f03_horizons():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert "20D" in f03["validation_methods"]["horizon_split"]["horizons"]
    assert "60D" in f03["validation_methods"]["horizon_split"]["horizons"]

def test_f06_horizons():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert "20D" in f06["validation_methods"]["horizon_split"]["horizons"]
    assert "60D" in f06["validation_methods"]["horizon_split"]["horizons"]

def test_f03_forbidden():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert "MULTI_FACTOR_COMPOSITE" in f03["forbidden_validation_methods_this_round"]
    assert "ALPHA_CLAIM" in f03["forbidden_validation_methods_this_round"]

def test_f06_forbidden():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert "MULTI_FACTOR_COMPOSITE" in f06["forbidden_validation_methods_this_round"]
    assert "ALPHA_CLAIM" in f06["forbidden_validation_methods_this_round"]

def test_f03_hypothesis():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert "industry-relative" in f03["expected_hypothesis"].lower()

def test_f06_hypothesis():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert "quality" in f06["expected_hypothesis"].lower()

def test_f03_diagnostics():
    f03 = next(f for f in mc["factors"] if f["factor_id"] == "F03")
    assert "sector-neutral check" in f03.get("required_diagnostics", [])
    assert "industry concentration check" in f03.get("required_diagnostics", [])

def test_f06_diagnostics():
    f06 = next(f for f in mc["factors"] if f["factor_id"] == "F06")
    assert "disclosure freshness" in f06.get("required_diagnostics", [])
    assert "quality score dispersion" in f06.get("required_diagnostics", [])

def test_alpha_false():
    assert mc.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert mc.get("production") == "BLOCKED"
