"""Tests for V13.F5.5.2.1 Rerun Partial Monitoring Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_closeout_exists():
    assert (D / "v13_f5_5_2_1_rerun_partial_monitoring_closeout.json").exists()


def test_closeout_status():
    co = _l("v13_f5_5_2_1_rerun_partial_monitoring_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-2-1-RERUN-PARTIAL-MONITORING-CLOSEOUT"
    assert co["status"] == "V13_F5_5_2_1_RERUN_PARTIAL_MONITORING_PASS"


def test_monitoring_results():
    co = _l("v13_f5_5_2_1_rerun_partial_monitoring_closeout.json")
    assert co["partial_monitoring_rerun_executed"] is True
    assert co["monitoring_scope"] == ["F21", "F24", "F30", "F31"]
    assert co["label_month"] == "2026-05"
    assert co["rebalance_date"] == "2026-05-06"
    assert co["ticker_count"] == 5
    assert co["horizons_used"] == ["5D", "20D"]


def test_spread_computed():
    co = _l("v13_f5_5_2_1_rerun_partial_monitoring_closeout.json")
    assert co["directional_spread_computed"] is True
    assert co["factors_with_spread"] == 4
    assert co["sample_scope"] == "MICRO_SAMPLE_5_TICKERS"


def test_no_formal_validation():
    co = _l("v13_f5_5_2_1_rerun_partial_monitoring_closeout.json")
    assert co["formal_oos_validation_executed"] is False
    assert co["formal_statistical_inference_allowed"] is False
    assert co["candidate_state_update_executed"] is False
    assert co["suspension_decision_executed"] is False
    assert co["rejection_decision_executed"] is False


def test_blocked():
    co = _l("v13_f5_5_2_1_rerun_partial_monitoring_closeout.json")
    assert co["ready_for_promotion_review"] == []
    assert co["promotion_allowed"] is False
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["v13_6_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


def test_next_action():
    co = _l("v13_f5_5_2_1_rerun_partial_monitoring_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_4_SIGNAL_SOURCE_RECOVERY_FOR_BATCH1_BATCH2_OR_EXPAND_MONITORING_SAMPLE"
