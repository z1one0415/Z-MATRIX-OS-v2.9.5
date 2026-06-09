"""Tests for V13.F5.5.2 First Partial Monitoring Safety Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_first_partial_monitoring_safety_audit.json").exists()


def test_safety_pass():
    s = _l("v13_f5_5_2_first_partial_monitoring_safety_audit.json")
    assert s["pipeline_signature"] == "Z2-V13-F5-5-2-FIRST-PARTIAL-MONITORING-SAFETY-AUDIT"
    assert s["status"] == "V13_F5_5_2_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0


def test_monitoring_executed():
    s = _l("v13_f5_5_2_first_partial_monitoring_safety_audit.json")
    assert s["checks"]["monitoring_execution_executed"] is True
    assert s["monitoring_scope_note"] == "MICRO_SAMPLE_PARTIAL_DIAGNOSTIC_ONLY"


def test_no_formal_validation():
    s = _l("v13_f5_5_2_first_partial_monitoring_safety_audit.json")
    assert s["checks"]["formal_oos_validation_executed"] is False
    assert s["checks"]["candidate_decision_update_executed"] is False
    assert s["checks"]["candidate_freeze_executed"] is False


def test_no_promotion():
    s = _l("v13_f5_5_2_first_partial_monitoring_safety_audit.json")
    assert s["checks"]["promotion_allowed"] is False
    assert s["checks"]["ready_for_promotion_review_empty"] is True
    assert s["checks"]["multi_factor_composite_built"] is False
    assert s["checks"]["weight_optimization_executed"] is False


def test_blocked():
    s = _l("v13_f5_5_2_first_partial_monitoring_safety_audit.json")
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["v13_6_allowed"] is False
    assert s["checks"]["paper_trading_allowed"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True
    assert s["checks"]["broker_runtime_blocked"] is True
    assert s["checks"]["real_trade_blocked"] is True
