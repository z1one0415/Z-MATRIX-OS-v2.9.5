"""Tests for V13.F5.5.3.1 Signal Materialization Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_closeout_exists():
    assert (D / "v13_f5_5_3_1_signal_materialization_closeout.json").exists()


def test_closeout_status():
    co = _l("v13_f5_5_3_1_signal_materialization_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-3-1-SIGNAL-MATERIALIZATION-CLOSEOUT"
    assert co["status"] == "V13_F5_5_3_1_MINIMAL_SIGNAL_SCORE_MATERIALIZATION_PASS"


def test_materialization_results():
    co = _l("v13_f5_5_3_1_signal_materialization_closeout.json")
    assert co["signal_materialization_executed"] is True
    assert co["materialized_factors"] == ["F21", "F24", "F30", "F31"]
    assert co["rebalance_date"] == "2026-05-06"
    assert co["ticker_count"] == 5
    assert co["rows_per_factor"] == 5
    assert co["total_signal_rows"] == 20
    assert co["signal_role"] == "FACTOR_SIGNAL_ONLY"


def test_no_full_computation():
    co = _l("v13_f5_5_3_1_signal_materialization_closeout.json")
    assert co["full_universe_computation_executed"] is False
    assert co["feature_store_write_executed"] is False
    assert co["runtime_reports_write_executed"] is False
    assert co["monitoring_rerun_executed"] is False
    assert co["candidate_state_update_executed"] is False


def test_readiness():
    co = _l("v13_f5_5_3_1_signal_materialization_closeout.json")
    assert co["ready_for_f5_5_2_rerun_partial_4_factor"] is True
    assert co["ready_for_full_10_factor_monitoring"] is False


def test_blocked():
    co = _l("v13_f5_5_3_1_signal_materialization_closeout.json")
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
    co = _l("v13_f5_5_3_1_signal_materialization_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_2_1_RERUN_PARTIAL_MONITORING_FOR_4_SIGNAL_READY_FACTORS"
