"""V13.F2.3 — Stage F: regime/horizon diagnostics tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

diag = L("v13_f2_3_regime_horizon_diagnostics.json")

def test_diagnostics_executed():
    assert diag.get("diagnostics_executed") is True

def test_validated_factors():
    assert "F03" in diag.get("validated_factors", [])
    assert "F06" in diag.get("validated_factors", [])

def test_per_factor_count():
    assert len(diag.get("per_factor_diagnostics", [])) == 2

def test_f03_diagnostics():
    f03 = next((f for f in diag.get("per_factor_diagnostics", []) if f["factor_id"] == "F03"), None)
    assert f03 is not None
    assert f03.get("diagnostics_executed") is True
    assert f03.get("sample_month_count", 0) >= 12

def test_f06_diagnostics():
    f06 = next((f for f in diag.get("per_factor_diagnostics", []) if f["factor_id"] == "F06"), None)
    assert f06 is not None
    assert f06.get("diagnostics_executed") is True

def test_f03_regime_ic():
    f03 = next((f for f in diag.get("per_factor_diagnostics", []) if f["factor_id"] == "F03"), None)
    regimes = f03.get("regime_split_ic_20d", {})
    assert "up_mean_ic" in regimes
    assert "down_mean_ic" in regimes
    assert "sideways_mean_ic" in regimes

def test_f03_regime_60d():
    f03 = next((f for f in diag.get("per_factor_diagnostics", []) if f["factor_id"] == "F03"), None)
    assert "regime_split_ic_60d" in f03

def test_alpha_false():
    assert diag.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert diag.get("production") == "BLOCKED"
