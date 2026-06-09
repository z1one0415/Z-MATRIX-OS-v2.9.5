"""Tests for V13.F5.5.4 Signal Source Recovery Safety."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_4_signal_source_recovery_safety_audit.json").exists()


def test_safety_pass():
    s = _l("v13_f5_5_4_signal_source_recovery_safety_audit.json")
    assert s["status"] == "V13_F5_5_4_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0


def test_no_execution():
    s = _l("v13_f5_5_4_signal_source_recovery_safety_audit.json")
    assert s["checks"]["signal_score_generation_executed"] is False
    assert s["checks"]["monitoring_rerun_executed"] is False
    assert s["checks"]["candidate_state_update_executed"] is False


def test_no_signal_files():
    s = _l("v13_f5_5_4_signal_source_recovery_safety_audit.json")
    assert s["checks"]["no_signal_scores_csv_in_sources"] is True
    assert s["checks"]["no_bucket_assignments_csv_in_sources"] is True


def test_blocked():
    s = _l("v13_f5_5_4_signal_source_recovery_safety_audit.json")
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True
    assert s["checks"]["broker_runtime_blocked"] is True
    assert s["checks"]["real_trade_blocked"] is True
