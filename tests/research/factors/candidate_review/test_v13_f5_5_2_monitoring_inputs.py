"""Tests for V13.F5.5.2 Monitoring Inputs Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_monitoring_input_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_2_monitoring_input_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-2-MONITORING-INPUT-AUDIT"
    assert a["status"] == "V13_F5_5_2_MONITORING_INPUT_AUDIT_PASS"
    assert a["violation_count"] == 0


def test_label_data():
    a = _l("v13_f5_5_2_monitoring_input_audit.json")
    assert a["checks"]["label_data_row_count"] == 10
    assert a["checks"]["label_data_row_count_gte_1"] is True
    assert a["checks"]["horizon_only_5d_20d"] is True
    assert a["checks"]["60D_not_present"] is True
    assert a["checks"]["label_role_outcome_only"] is True
    assert a["checks"]["no_forbidden_columns"] is True


def test_scope():
    a = _l("v13_f5_5_2_monitoring_input_audit.json")
    assert a["checks"]["monitoring_scope_count"] == 10
    assert a["checks"]["monitoring_scope_matches_10_frozen"] is True
    assert len(a["monitoring_scope"]) == 10


def test_blocked():
    a = _l("v13_f5_5_2_monitoring_input_audit.json")
    assert a["checks"]["runner_enabled_false"] is True
    assert a["checks"]["execution_allowed_false"] is True
