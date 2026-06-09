"""Tests for V13.F5.5.2.1 Rerun Partial Monitoring Safety."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_1_rerun_partial_monitoring_safety_audit.json").exists()


def test_safety_pass():
    s = _l("v13_f5_5_2_1_rerun_partial_monitoring_safety_audit.json")
    assert s["pipeline_signature"] == "Z2-V13-F5-5-2-1-RERUN-PARTIAL-MONITORING-SAFETY-AUDIT"
    assert s["status"] == "V13_F5_5_2_1_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0


def test_monitoring_executed():
    s = _l("v13_f5_5_2_1_rerun_partial_monitoring_safety_audit.json")
    assert s["checks"]["partial_monitoring_rerun_executed"] is True
    assert s["checks"]["formal_oos_validation_executed"] is False


def test_no_state_changes():
    s = _l("v13_f5_5_2_1_rerun_partial_monitoring_safety_audit.json")
    assert s["checks"]["candidate_state_update_executed"] is False
    assert s["checks"]["suspension_decision_executed"] is False
    assert s["checks"]["rejection_decision_executed"] is False
    assert s["checks"]["promotion_allowed"] is False


def test_blocked():
    s = _l("v13_f5_5_2_1_rerun_partial_monitoring_safety_audit.json")
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True
    assert s["checks"]["broker_runtime_blocked"] is True
    assert s["checks"]["real_trade_blocked"] is True
