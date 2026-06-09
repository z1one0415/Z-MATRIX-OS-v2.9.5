"""Tests for V13.F5.5.4.1 Signal Materialization Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")

def _l(n): return json.loads((D / n).read_text())

def test_closeout_exists():
    assert (D / "v13_f5_5_4_1_signal_materialization_closeout.json").exists()

def test_closeout_partial():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-4-1-BATCH1-BATCH2-SIGNAL-MATERIALIZATION-CLOSEOUT"
    assert co["status"] == "V13_F5_5_4_1_SIGNAL_MATERIALIZATION_PARTIAL"

def test_materialization_results():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    assert co["materialized_factors"] == ["F04", "F10", "F11"]
    assert co["blocked_factors"] == ["F14", "F15", "F16"]
    assert co["total_signal_rows_this_step"] == 15
    assert co["total_signal_ready_factors"] == 7

def test_blocked_reasons():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    for fid in ["F14", "F15", "F16"]:
        assert co["blocked_reasons"][fid] == "BLOCKED_BY_SOURCE_DATA"

def test_readiness():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    assert co["ready_for_10_factor_partial_monitoring"] is False
    assert co["ready_for_7_factor_partial_monitoring"] is True

def test_no_execution():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    assert co["full_universe_computation_executed"] is False
    assert co["feature_store_write_executed"] is False
    assert co["monitoring_rerun_executed"] is False
    assert co["candidate_state_update_executed"] is False

def test_blocked():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    assert co["promotion_allowed"] is False
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"

def test_next_action():
    co = _l("v13_f5_5_4_1_signal_materialization_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_4_2_REPAIR_BLOCKED_SIGNAL_SOURCES_OR_RERUN_PARTIAL_AVAILABLE_FACTORS"
