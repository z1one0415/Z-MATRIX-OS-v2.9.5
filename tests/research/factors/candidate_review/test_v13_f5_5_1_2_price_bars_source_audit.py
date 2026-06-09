"""Tests for V13.F5.5.1.2 Price Bars Source Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_1_2_price_bars_source_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_1_2_price_bars_source_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-1-2-PRICE-BARS-SOURCE-AUDIT"
    assert a["status"] == "V13_F5_5_1_2_PRICE_BARS_SOURCE_AUDIT_PASS"
    assert a["source_type"] == "LOCAL_READ_ONLY"
    assert a["violation_count"] == 0


def test_forward_windows():
    a = _l("v13_f5_5_1_2_price_bars_source_audit.json")
    assert a["checks"]["price_bars_exists"] is True
    assert a["checks"]["source_is_local_read_only"] is True
    assert a["checks"]["5D_forward_window_complete"] is True
    assert a["checks"]["20D_forward_window_complete"] is True
    assert a["checks"]["60D_forward_window_complete"] is False


def test_no_forbidden_reads():
    a = _l("v13_f5_5_1_2_price_bars_source_audit.json")
    assert a["checks"]["no_factor_score_read"] is True
    assert a["checks"]["no_rank_bucket_read"] is True
    assert a["checks"]["no_feature_store_read"] is True
    assert a["checks"]["no_external_data_source_call"] is True
