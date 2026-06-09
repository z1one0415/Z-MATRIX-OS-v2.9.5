"""Tests for V13.F5.5.2 Micro-Sample Monitoring Diagnostic."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_diagnostic_exists():
    assert (D / "v13_f5_5_2_micro_sample_monitoring_diagnostic.json").exists()


def test_diagnostic_status():
    d = _l("v13_f5_5_2_micro_sample_monitoring_diagnostic.json")
    assert d["pipeline_signature"] == "Z2-V13-F5-5-2-MICRO-SAMPLE-MONITORING-DIAGNOSTIC"
    assert "EXECUTED" in d["status"]


def test_micro_sample_scope():
    d = _l("v13_f5_5_2_micro_sample_monitoring_diagnostic.json")
    assert d["sample_scope"] == "MICRO_SAMPLE"
    assert d["formal_statistical_inference_allowed"] is False
    assert d["rank_ic_reported_as_formal_evidence"] is False
    assert d["candidate_state_change_allowed"] is False


def test_label_coverage():
    d = _l("v13_f5_5_2_micro_sample_monitoring_diagnostic.json")
    lc = d["label_coverage"]
    assert lc["total_label_rows"] == 10
    assert lc["5D_rows"] == 5
    assert lc["20D_rows"] == 5
    assert lc["usable_ticker_count"] == 5


def test_label_statistics():
    d = _l("v13_f5_5_2_micro_sample_monitoring_diagnostic.json")
    stats = d["label_statistics"]
    assert stats["5D"]["count"] == 5
    assert stats["20D"]["count"] == 5
    assert "mean_return" in stats["5D"]
    assert "sign_consistency" in stats["5D"]


def test_factor_diagnostics():
    d = _l("v13_f5_5_2_micro_sample_monitoring_diagnostic.json")
    assert d["factor_signal_summary"]["total_factors_checked"] == 10
    assert d["factor_signal_summary"]["factors_blocked"] == 10
    assert len(d["factor_diagnostics"]) == 10
    for fd in d["factor_diagnostics"]:
        assert fd["signal_available"] is False
        assert fd["diagnostic_status"] == "SIGNAL_INPUT_BLOCKED_CANNOT_COMPUTE"
        assert fd["5D_directional_spread"] is None
        assert fd["20D_directional_spread"] is None


def test_no_forbidden_outputs():
    """Ensure no alpha/trade/position/expected_return outputs."""
    d = _l("v13_f5_5_2_micro_sample_monitoring_diagnostic.json")
    text = json.dumps(d)
    forbidden = ["alpha_claim", "expected_return_claim", "portfolio_weight",
                 "trade_signal", "buy_signal", "sell_signal",
                 "formal_ic_claim", "promotion_signal", "suspension_decision"]
    for term in forbidden:
        # Only check if value is non-false/non-null
        if f'"{term}": true' in text or f'"{term}": "' in text:
            assert False, f"Forbidden output found: {term}"
