"""Tests for V13.F5.5.2.1 Rerun Input Join Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_1_rerun_input_join_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_2_1_rerun_input_join_audit.json")
    assert a["status"] == "V13_F5_5_2_1_INPUT_JOIN_AUDIT_PASS"
    assert a["violation_count"] == 0


def test_join_complete():
    a = _l("v13_f5_5_2_1_rerun_input_join_audit.json")
    assert a["checks"]["label_panel_exists"] is True
    assert a["checks"]["signal_scores_exist"] is True
    assert a["checks"]["per_factor_ticker_count_5"] is True
    for fid in ["F21", "F24", "F30", "F31"]:
        assert a["factor_join_results"][fid]["join_complete"] is True


def test_no_leakage():
    a = _l("v13_f5_5_2_1_rerun_input_join_audit.json")
    assert a["checks"]["signal_no_forward_return"] is True
    assert a["checks"]["label_no_score_rank_bucket"] is True
    assert a["checks"]["join_no_alpha_trade_order"] is True
    assert a["checks"]["60D_not_present"] is True
