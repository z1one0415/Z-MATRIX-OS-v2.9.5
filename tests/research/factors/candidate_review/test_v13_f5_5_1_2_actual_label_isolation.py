"""Tests for V13.F5.5.1.2 Actual Label Isolation."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_1_2_actual_label_isolation_audit.json").exists()


def test_isolation_pass():
    a = _l("v13_f5_5_1_2_actual_label_isolation_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-1-2-ACTUAL-LABEL-ISOLATION-AUDIT"
    assert a["status"] == "V13_F5_5_1_2_LABEL_ISOLATION_PASS"
    assert a["violation_count"] == 0


def test_isolation_checks():
    a = _l("v13_f5_5_1_2_actual_label_isolation_audit.json")
    assert a["checks"]["written_to_feature_store"] is False
    assert a["checks"]["used_for_factor_calculation"] is False
    assert a["checks"]["used_for_candidate_decision"] is False
    assert a["checks"]["used_for_monitoring_execution"] is False
    assert a["checks"]["monitoring_execution_executed"] is False
    assert a["checks"]["true_oos_validation_executed"] is False
