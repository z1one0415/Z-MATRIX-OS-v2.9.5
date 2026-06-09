"""Tests for V13.F5.5.6 Safety Audit and Closeout."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
def _l(n): return json.loads((D / n).read_text())

def test_safety_pass():
    s = _l("v13_f5_5_6_expansion_gate_safety_audit.json")
    assert s["status"] == "V13_F5_5_6_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0
    assert s["checks"]["planning_only"] is True
    assert s["checks"]["sample_expansion_execution_executed"] is False
    assert s["checks"]["monitoring_execution_executed"] is False
    assert s["checks"]["formal_oos_validation_executed"] is False
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True

def test_closeout_pass():
    co = _l("v13_f5_5_6_expansion_gate_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-6-MONITORING-SAMPLE-EXPANSION-GATE-CLOSEOUT"
    assert co["status"] == "V13_F5_5_6_EXPANSION_GATE_PLAN_PASS"
    assert co["planning_only"] is True

def test_closeout_gap():
    co = _l("v13_f5_5_6_expansion_gate_closeout.json")
    assert co["current_ticker_count"] == 5
    assert co["current_oos_month_count"] == 1
    assert co["minimum_formal_ticker_count"] == 475
    assert co["minimum_formal_oos_months"] == 6
    assert co["gap_to_formal_gate"]["tickers_needed"] == 470
    assert co["gap_to_formal_gate"]["months_needed"] == 5

def test_closeout_paths():
    co = _l("v13_f5_5_6_expansion_gate_closeout.json")
    assert co["seven_factor_expanded_path_allowed_after_data_ready"] is True
    assert co["ten_factor_full_path_blocked_until_f14_f15_f16_repaired"] is True

def test_closeout_blocked():
    co = _l("v13_f5_5_6_expansion_gate_closeout.json")
    assert co["promotion_allowed"] is False
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"

def test_next_action():
    co = _l("v13_f5_5_6_expansion_gate_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_7_EXPANDED_7_FACTOR_DIAGNOSTIC_OR_F14_F15_F16_DATA_CONTRACT_IMPLEMENTATION"
