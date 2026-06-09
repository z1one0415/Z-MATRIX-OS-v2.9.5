"""Tests for V13.F5.5.4.1 Signal Isolation."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")

def _l(n): return json.loads((D / n).read_text())

def test_isolation_pass():
    a = _l("v13_f5_5_4_1_signal_isolation_audit.json")
    assert a["status"] == "V13_F5_5_4_1_SIGNAL_ISOLATION_PASS"
    assert a["violation_count"] == 0

def test_isolation_checks():
    a = _l("v13_f5_5_4_1_signal_isolation_audit.json")
    assert a["checks"]["no_forward_return_in_signal_files"] is True
    assert a["checks"]["no_alpha_trade_position_order"] is True
    assert a["checks"]["no_feature_store_write"] is True
    assert a["checks"]["all_signal_roles_correct"] is True
