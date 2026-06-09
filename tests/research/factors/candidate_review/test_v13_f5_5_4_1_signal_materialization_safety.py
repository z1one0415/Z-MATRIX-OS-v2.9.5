"""Tests for V13.F5.5.4.1 Signal Materialization Safety."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")

def _l(n): return json.loads((D / n).read_text())

def test_safety_pass():
    s = _l("v13_f5_5_4_1_signal_materialization_safety_audit.json")
    assert s["status"] == "V13_F5_5_4_1_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0

def test_scope():
    s = _l("v13_f5_5_4_1_signal_materialization_safety_audit.json")
    assert s["checks"]["signal_materialization_executed"] is True
    assert s["checks"]["factor_recalculation_scope"] == "MINIMAL_LABEL_TICKERS_ONLY"
    assert s["checks"]["full_universe_computation_executed"] is False

def test_no_leakage():
    s = _l("v13_f5_5_4_1_signal_materialization_safety_audit.json")
    assert s["checks"]["forward_return_used_for_signal"] is False
    assert s["checks"]["outcome_label_used_for_signal"] is False
    assert s["checks"]["signal_isolation_pass"] is True

def test_blocked():
    s = _l("v13_f5_5_4_1_signal_materialization_safety_audit.json")
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["alpha_claim_allowed"] is False
    assert s["checks"]["production_blocked"] is True
    assert s["checks"]["broker_runtime_blocked"] is True
    assert s["checks"]["real_trade_blocked"] is True
