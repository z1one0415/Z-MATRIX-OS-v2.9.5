"""Tests for V13.F5.5.2.2 Seven-Factor Directional Spread Diagnostic."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
def _l(n): return json.loads((D / n).read_text())

def test_diagnostic_computed():
    d = _l("v13_f5_5_2_2_seven_factor_directional_spread_diagnostic.json")
    assert d["status"] == "V13_F5_5_2_2_DIRECTIONAL_SPREAD_DIAGNOSTIC_COMPUTED"
    assert d["summary"]["factors_with_spread_computed"] == 7

def test_micro_sample_guards():
    d = _l("v13_f5_5_2_2_seven_factor_directional_spread_diagnostic.json")
    assert d["sample_scope"] == "MICRO_SAMPLE_5_TICKERS"
    assert d["formal_oos_validation_executed"] is False
    assert d["formal_statistical_inference_allowed"] is False
    assert d["rank_ic_reported_as_formal_evidence"] is False
    assert d["candidate_state_change_allowed"] is False
    assert d["alpha_claim_allowed"] is False

def test_all_7_factors():
    d = _l("v13_f5_5_2_2_seven_factor_directional_spread_diagnostic.json")
    assert len(d["factor_diagnostics"]) == 7
    factor_ids = [fd["factor_id"] for fd in d["factor_diagnostics"]]
    assert set(factor_ids) == {"F04", "F10", "F11", "F21", "F24", "F30", "F31"}
    for fd in d["factor_diagnostics"]:
        assert fd["5D_spread"] is not None
        assert fd["20D_spread"] is not None
        assert fd["5D_spread"]["usable_ticker_count"] == 5

def test_blocked_excluded():
    d = _l("v13_f5_5_2_2_seven_factor_directional_spread_diagnostic.json")
    assert d["blocked_factors_excluded"] == ["F14", "F15", "F16"]
