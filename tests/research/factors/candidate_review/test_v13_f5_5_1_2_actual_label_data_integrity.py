"""Tests for V13.F5.5.1.2 Actual Label Data Integrity."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_1_2_actual_label_data_integrity_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_1_2_actual_label_data_integrity_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-1-2-ACTUAL-LABEL-DATA-INTEGRITY-AUDIT"
    assert a["status"] == "V13_F5_5_1_2_LABEL_DATA_INTEGRITY_PASS"
    assert a["violation_count"] == 0
    assert a["label_data_row_count"] > 0


def test_row_counts():
    a = _l("v13_f5_5_1_2_actual_label_data_integrity_audit.json")
    assert a["checks"]["label_data_row_count_gt_zero"] is True
    assert a["checks"]["5D_row_count_gt_zero"] is True
    assert a["checks"]["20D_row_count_gt_zero"] is True
    assert a["checks"]["60D_row_count_zero"] is True


def test_data_quality():
    a = _l("v13_f5_5_1_2_actual_label_data_integrity_audit.json")
    assert a["checks"]["forward_return_non_empty"] is True
    assert a["checks"]["ticker_rebalance_horizon_unique"] is True
    assert a["checks"]["label_available_at_gte_source_end_date"] is True


def test_no_forbidden_fields():
    a = _l("v13_f5_5_1_2_actual_label_data_integrity_audit.json")
    assert a["checks"]["no_factor_score_rank_bucket"] is True
    assert a["checks"]["no_alpha_trade_position_order"] is True
