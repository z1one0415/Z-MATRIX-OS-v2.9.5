"""Tests for V13.F5.5.2.1 Directional Spread Diagnostic."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_diagnostic_exists():
    assert (D / "v13_f5_5_2_1_directional_spread_diagnostic.json").exists()


def test_diagnostic_status():
    d = _l("v13_f5_5_2_1_directional_spread_diagnostic.json")
    assert d["pipeline_signature"] == "Z2-V13-F5-5-2-1-DIRECTIONAL-SPREAD-DIAGNOSTIC"
    assert d["status"] == "V13_F5_5_2_1_DIRECTIONAL_SPREAD_DIAGNOSTIC_COMPUTED"


def test_micro_sample_guards():
    d = _l("v13_f5_5_2_1_directional_spread_diagnostic.json")
    assert d["sample_scope"] == "MICRO_SAMPLE_5_TICKERS"
    assert d["formal_oos_validation_executed"] is False
    assert d["formal_statistical_inference_allowed"] is False
    assert d["rank_ic_reported_as_formal_evidence"] is False
    assert d["candidate_state_change_allowed"] is False


def test_all_4_factors_computed():
    d = _l("v13_f5_5_2_1_directional_spread_diagnostic.json")
    assert d["summary"]["factors_with_spread_computed"] == 4
    assert len(d["factor_diagnostics"]) == 4
    for fd in d["factor_diagnostics"]:
        assert fd["signal_available"] is True
        assert fd["diagnostic_status"] == "COMPUTED"
        assert fd["5D_spread"] is not None
        assert fd["20D_spread"] is not None


def test_spread_structure():
    d = _l("v13_f5_5_2_1_directional_spread_diagnostic.json")
    for fd in d["factor_diagnostics"]:
        for horizon in ["5D_spread", "20D_spread"]:
            s = fd[horizon]
            assert "spread" in s
            assert "top_mean_return" in s
            assert "bottom_mean_return" in s
            assert "sign_consistency" in s
            assert "usable_ticker_count" in s
            assert s["usable_ticker_count"] == 5


def test_no_forbidden_outputs():
    d = _l("v13_f5_5_2_1_directional_spread_diagnostic.json")
    text = json.dumps(d)
    for term in ["expected_return_claim", "portfolio_weight",
                 "promotion_signal", "suspension_decision"]:
        assert f'"{term}"' not in text or f'"{term}": false' in text or f'"{term}": null' in text
