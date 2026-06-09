"""Tests for V13.F5.5.2 First Partial Monitoring Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_closeout_exists():
    assert (D / "v13_f5_5_2_first_partial_monitoring_closeout.json").exists()


def test_closeout_status():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-2-FIRST-PARTIAL-MONITORING-CLOSEOUT"
    assert co["status"] == "V13_F5_5_2_FIRST_PARTIAL_MONITORING_PASS"


def test_monitoring_executed():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["monitoring_execution_executed"] is True
    assert co["monitoring_execution_scope"] == "MICRO_SAMPLE_PARTIAL_DIAGNOSTIC_ONLY"
    assert co["label_month"] == "2026-05"
    assert co["label_data_row_count"] == 10
    assert co["ticker_count"] == 5
    assert co["generated_horizons_used"] == ["5D", "20D"]
    assert co["blocked_horizons"] == ["60D"]


def test_factor_signals():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["factor_signals_available"] == 0
    assert co["factor_signals_blocked"] == 10
    assert co["directional_spread_computed"] is False


def test_no_formal_validation():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["formal_oos_validation_executed"] is False
    assert co["formal_statistical_inference_allowed"] is False
    assert co["candidate_state_update_executed"] is False
    assert co["suspension_decision_executed"] is False
    assert co["rejection_decision_executed"] is False


def test_no_promotion():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["promotion_allowed"] is False
    assert co["ready_for_promotion_review"] == []


def test_blocked():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["v13_6_allowed"] is False
    assert co["paper_trading_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


def test_next_action():
    co = _l("v13_f5_5_2_first_partial_monitoring_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_3_MONITORING_SAMPLE_EXPANSION_OR_NEXT_OOS_MONTH_PLAN"
