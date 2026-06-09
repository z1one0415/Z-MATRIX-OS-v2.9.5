"""Tests for V13.F5.5.6 Expansion Gate Contract and Requirements."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
def _l(n): return json.loads((D / n).read_text())

def test_all_artifacts_exist():
    expected = [
        "v13_f5_5_6_expansion_gate_contract.json",
        "v13_f5_5_6_current_evidence_limitation_audit.json",
        "v13_f5_5_6_u475_expansion_requirement.json",
        "v13_f5_5_6_oos_month_calendar_plan.json",
        "v13_f5_5_6_seven_vs_ten_factor_gate_split.json",
        "v13_f5_5_6_g18_handoff_gate_plan.json",
        "v13_f5_5_6_expansion_gate_safety_audit.json",
        "v13_f5_5_6_expansion_gate_closeout.json"
    ]
    for f in expected:
        assert (D / f).exists(), f"Missing: {f}"

def test_contract_planning_only():
    c = _l("v13_f5_5_6_expansion_gate_contract.json")
    assert c["planning_only"] is True
    assert c["current_sample_scope"] == "MICRO_SAMPLE_5_TICKERS_1_MONTH"
    assert c["minimum_formal_ticker_count"] == 475
    assert c["minimum_formal_oos_months"] == 6

def test_contract_blocked():
    c = _l("v13_f5_5_6_expansion_gate_contract.json")
    assert c["formal_oos_validation_allowed"] is False
    assert c["sample_expansion_execution_allowed"] is False
    assert c["new_label_generation_allowed"] is False
    assert c["monitoring_execution_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"

def test_u475_requirement():
    r = _l("v13_f5_5_6_u475_expansion_requirement.json")
    assert r["price_bars_requirements"]["minimum_ticker_coverage"] == 475
    assert r["price_bars_requirements"]["forward_window_60D"] is True
    assert r["minimum_for_formal_oos_gate"]["oos_months"] == 6

def test_oos_calendar():
    p = _l("v13_f5_5_6_oos_month_calendar_plan.json")
    assert p["minimum_formal_months"] == 6
    assert p["preferred_months"] == 12
    assert p["first_available_month"] == "2026-05"
