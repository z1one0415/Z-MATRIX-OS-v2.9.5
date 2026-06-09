"""Tests for V13.F5.5.3.1 Signal Materialization Safety."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_3_1_signal_materialization_safety_audit.json").exists()


def test_safety_pass():
    s = _l("v13_f5_5_3_1_signal_materialization_safety_audit.json")
    assert s["pipeline_signature"] == "Z2-V13-F5-5-3-1-SIGNAL-MATERIALIZATION-SAFETY-AUDIT"
    assert s["status"] == "V13_F5_5_3_1_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0


def test_materialization_scope():
    s = _l("v13_f5_5_3_1_signal_materialization_safety_audit.json")
    assert s["checks"]["signal_materialization_executed"] is True
    assert s["checks"]["factor_recalculation_scope"] == "MINIMAL_LABEL_TICKERS_ONLY"
    assert s["checks"]["full_universe_computation_executed"] is False


def test_no_leakage():
    s = _l("v13_f5_5_3_1_signal_materialization_safety_audit.json")
    assert s["checks"]["forward_return_used_for_signal"] is False
    assert s["checks"]["outcome_label_used_for_signal"] is False
    assert s["checks"]["signal_isolation_pass"] is True


def test_no_writes():
    s = _l("v13_f5_5_3_1_signal_materialization_safety_audit.json")
    assert s["checks"]["feature_store_write_executed"] is False
    assert s["checks"]["runtime_reports_write_executed"] is False
    assert s["checks"]["monitoring_rerun_executed"] is False
    assert s["checks"]["candidate_state_update_executed"] is False


def test_blocked():
    s = _l("v13_f5_5_3_1_signal_materialization_safety_audit.json")
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True
    assert s["checks"]["broker_runtime_blocked"] is True
    assert s["checks"]["real_trade_blocked"] is True
