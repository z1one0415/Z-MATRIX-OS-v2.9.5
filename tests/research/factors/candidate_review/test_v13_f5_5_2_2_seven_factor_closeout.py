"""Tests for V13.F5.5.2.2 Seven-Factor Partial Monitoring Closeout."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
def _l(n): return json.loads((D / n).read_text())

def test_closeout_pass():
    co = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-2-2-SEVEN-FACTOR-PARTIAL-MONITORING-CLOSEOUT"
    assert co["status"] == "V13_F5_5_2_2_SEVEN_FACTOR_PARTIAL_MONITORING_PASS"

def test_monitoring_results():
    co = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_closeout.json")
    assert co["seven_factor_partial_monitoring_executed"] is True
    assert co["monitoring_scope"] == ["F04", "F10", "F11", "F21", "F24", "F30", "F31"]
    assert co["blocked_factors"] == ["F14", "F15", "F16"]
    assert co["ticker_count"] == 5
    assert co["signal_rows"] == 35
    assert co["directional_spread_computed"] is True
    assert co["factors_with_spread"] == 7

def test_no_formal():
    co = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_closeout.json")
    assert co["formal_oos_validation_executed"] is False
    assert co["formal_statistical_inference_allowed"] is False
    assert co["candidate_state_update_executed"] is False
    assert co["suspension_decision_executed"] is False

def test_blocked():
    co = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_closeout.json")
    assert co["promotion_allowed"] is False
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"

def test_next_action():
    co = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_4_2_REPAIR_BLOCKED_SIGNAL_SOURCES_FOR_F14_F15_F16"
