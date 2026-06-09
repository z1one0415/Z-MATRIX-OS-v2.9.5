"""Tests for V13.F5.5.2.2 Seven-Factor Input Join."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
def _l(n): return json.loads((D / n).read_text())

def test_join_audit_pass():
    a = _l("v13_f5_5_2_2_seven_factor_input_join_audit.json")
    assert a["status"] == "V13_F5_5_2_2_INPUT_JOIN_AUDIT_PASS"
    assert a["violation_count"] == 0

def test_signal_rows():
    a = _l("v13_f5_5_2_2_seven_factor_input_join_audit.json")
    assert a["checks"]["signal_rows_total"] == 35
    assert a["checks"]["label_row_count"] == 10
    assert a["checks"]["per_factor_ticker_count_5"] is True

def test_no_leakage():
    a = _l("v13_f5_5_2_2_seven_factor_input_join_audit.json")
    assert a["checks"]["signal_no_forward_return"] is True
    assert a["checks"]["label_no_score_rank_bucket"] is True
    assert a["checks"]["blocked_factors_excluded"] is True
