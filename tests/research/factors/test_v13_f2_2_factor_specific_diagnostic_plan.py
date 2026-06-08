"""V13.F2.2 — Stage E: factor-specific diagnostic plan tests."""
import json
from tests._path_utils import RUNTIME_FACTORS

def L(name):
    p = RUNTIME_FACTORS / name
    return json.loads(p.read_text()) if p.exists() else {}

p = L("v13_f2_2_factor_specific_diagnostic_plan.json")

def test_plan_built():
    assert p.get("status") == "V13_F2_2_FACTOR_SPECIFIC_DIAGNOSTIC_PLAN_BUILT"

def test_diagnostic_scope():
    scope = p.get("diagnostic_scope", [])
    assert "F03" in scope
    assert "F06" in scope

def test_f03_sector_concentration():
    assert "sector_concentration" in p.get("f03_diagnostics", [])

def test_f03_industry_neutrality():
    assert "industry_neutrality" in p.get("f03_diagnostics", [])

def test_f03_sector_wind_overlap():
    assert "sector_wind_overlap" in p.get("f03_diagnostics", [])

def test_f03_regime_split():
    assert "regime_split" in p.get("f03_diagnostics", [])

def test_f03_20d_vs_60d():
    assert "20d_vs_60d_decay" in p.get("f03_diagnostics", [])

def test_f06_quality_dispersion():
    assert "quality_score_dispersion" in p.get("f06_diagnostics", [])

def test_f06_reporting_period():
    assert "reporting_period_distribution" in p.get("f06_diagnostics", [])

def test_f06_disclosure_freshness():
    assert "disclosure_freshness" in p.get("f06_diagnostics", [])

def test_f06_staleness():
    assert "fundamental_staleness" in p.get("f06_diagnostics", [])

def test_f06_20d_vs_60d():
    assert "20d_vs_60d_decay" in p.get("f06_diagnostics", [])

def test_not_executed():
    assert p.get("diagnostics_executed_this_round") == []

def test_allowed():
    assert p.get("diagnostics_allowed_next_step") is True

def test_alpha_false():
    assert p.get("alpha_claim_allowed") is False

def test_prod_blocked():
    assert p.get("production") == "BLOCKED"
