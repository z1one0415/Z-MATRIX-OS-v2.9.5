"""Tests for V13.F5.5.3.1 Signal Isolation."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_3_1_signal_isolation_audit.json").exists()


def test_isolation_pass():
    a = _l("v13_f5_5_3_1_signal_isolation_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-3-1-SIGNAL-ISOLATION-AUDIT"
    assert a["status"] == "V13_F5_5_3_1_SIGNAL_ISOLATION_PASS"
    assert a["violation_count"] == 0


def test_isolation_checks():
    a = _l("v13_f5_5_3_1_signal_isolation_audit.json")
    assert a["checks"]["no_forward_return_in_signal_files"] is True
    assert a["checks"]["no_outcome_label_in_signal_files"] is True
    assert a["checks"]["no_alpha_trade_position_order"] is True
    assert a["checks"]["no_feature_store_write"] is True
    assert a["checks"]["no_monitoring_rerun_triggered"] is True
    assert a["checks"]["no_candidate_state_update"] is True
    assert a["checks"]["all_signal_roles_correct"] is True
