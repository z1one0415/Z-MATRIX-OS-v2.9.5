"""Tests for V13.F5.5.2.1 Micro-Sample Interpretation Guardrail."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_guardrail_exists():
    assert (D / "v13_f5_5_2_1_micro_sample_interpretation_guardrail.json").exists()


def test_guardrail_active():
    g = _l("v13_f5_5_2_1_micro_sample_interpretation_guardrail.json")
    assert g["micro_sample_warning_required"] is True
    assert g["ticker_count"] == 5


def test_minimum_requirements():
    g = _l("v13_f5_5_2_1_micro_sample_interpretation_guardrail.json")
    assert g["minimum_for_formal_oos_validation"] == ">=475 tickers and >=6 OOS months"
    assert g["current_vs_minimum"]["gap_tickers"] == 470
    assert g["current_vs_minimum"]["gap_months"] == 5


def test_allowed_use():
    g = _l("v13_f5_5_2_1_micro_sample_interpretation_guardrail.json")
    assert "pipeline_diagnostic" in g["allowed_use"]
    assert "sanity_check" in g["allowed_use"]


def test_forbidden_use():
    g = _l("v13_f5_5_2_1_micro_sample_interpretation_guardrail.json")
    assert "alpha_claim" in g["forbidden_use"]
    assert "promotion_review" in g["forbidden_use"]
    assert "suspension_decision" in g["forbidden_use"]
    assert "trade_signal" in g["forbidden_use"]
