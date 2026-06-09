"""Tests for V13.F5.5.3 Signal Restoration Safety Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_3_signal_restoration_safety_audit.json").exists()


def test_safety_pass():
    s = _l("v13_f5_5_3_signal_restoration_safety_audit.json")
    assert s["pipeline_signature"] == "Z2-V13-F5-5-3-SIGNAL-RESTORATION-SAFETY-AUDIT"
    assert s["status"] == "V13_F5_5_3_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0
    assert s["planning_only_verified"] is True


def test_no_execution():
    s = _l("v13_f5_5_3_signal_restoration_safety_audit.json")
    assert s["checks"]["signal_materialization_executed"] is False
    assert s["checks"]["factor_recalculation_executed"] is False
    assert s["checks"]["monitoring_rerun_executed"] is False
    assert s["checks"]["candidate_state_update_executed"] is False


def test_blocked():
    s = _l("v13_f5_5_3_signal_restoration_safety_audit.json")
    assert s["checks"]["promotion_allowed"] is False
    assert s["checks"]["ready_for_promotion_review_empty"] is True
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["v13_6_allowed"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True
    assert s["checks"]["broker_runtime_blocked"] is True
    assert s["checks"]["real_trade_blocked"] is True
