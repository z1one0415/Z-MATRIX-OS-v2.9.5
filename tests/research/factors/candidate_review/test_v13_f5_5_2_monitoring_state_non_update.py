"""Tests for V13.F5.5.2 Monitoring State Non-Update Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_monitoring_state_non_update_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_2_monitoring_state_non_update_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-2-MONITORING-STATE-NON-UPDATE-AUDIT"
    assert a["status"] == "V13_F5_5_2_STATE_NON_UPDATE_PASS"
    assert a["violation_count"] == 0


def test_no_state_changes():
    a = _l("v13_f5_5_2_monitoring_state_non_update_audit.json")
    assert a["checks"]["registry_frozen_count_unchanged"] is True
    assert a["checks"]["no_suspension_executed"] is True
    assert a["checks"]["no_rejection_executed"] is True
    assert a["checks"]["no_promotion_executed"] is True
    assert a["checks"]["no_candidate_state_transition"] is True


def test_promotion_blocked():
    a = _l("v13_f5_5_2_monitoring_state_non_update_audit.json")
    assert a["checks"]["unified_registry_promotion_allowed_false"] is True
    assert a["checks"]["ready_for_promotion_review_empty"] is True
    assert a["state_changes_detected"] == []
