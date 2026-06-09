"""Tests for V13.F5.5.2.1 State Non-Update Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_1_state_non_update_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_2_1_state_non_update_audit.json")
    assert a["status"] == "V13_F5_5_2_1_STATE_NON_UPDATE_PASS"
    assert a["violation_count"] == 0
    assert a["state_changes_detected"] == []


def test_no_changes():
    a = _l("v13_f5_5_2_1_state_non_update_audit.json")
    assert a["checks"]["no_suspension_executed"] is True
    assert a["checks"]["no_rejection_executed"] is True
    assert a["checks"]["no_promotion_executed"] is True
    assert a["checks"]["no_candidate_state_transition"] is True


def test_factors_stable():
    a = _l("v13_f5_5_2_1_state_non_update_audit.json")
    for f in ["F21", "F24", "F30", "F31"]:
        assert a["checks"][f"{f}_not_upgraded"] is True
        assert a["checks"][f"{f}_not_downgraded"] is True
