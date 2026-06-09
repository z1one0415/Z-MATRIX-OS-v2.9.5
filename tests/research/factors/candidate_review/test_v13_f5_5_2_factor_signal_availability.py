"""Tests for V13.F5.5.2 Factor Signal Availability Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_2_factor_signal_availability_audit.json").exists()


def test_audit_status():
    a = _l("v13_f5_5_2_factor_signal_availability_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-2-FACTOR-SIGNAL-AVAILABILITY-AUDIT"
    assert "BLOCKED" in a["status"] or "PARTIAL" in a["status"]


def test_all_10_checked():
    a = _l("v13_f5_5_2_factor_signal_availability_audit.json")
    assert a["frozen_candidates_checked"] == 10
    assert len(a["factor_results"]) == 10


def test_signal_blocked():
    a = _l("v13_f5_5_2_factor_signal_availability_audit.json")
    # All signals blocked because no pre-computed scores exist
    assert a["factors_with_signal_blocked"] == 10
    for r in a["factor_results"]:
        assert r["factor_status"] == "SIGNAL_INPUT_BLOCKED"
        assert r["signal_available_for_label_tickers"] is False


def test_data_source_restrictions():
    a = _l("v13_f5_5_2_factor_signal_availability_audit.json")
    assert a["data_source_restrictions"]["runtime_reports_read"] is False
    assert a["data_source_restrictions"]["feature_store_read"] is False
    assert a["data_source_restrictions"]["external_data_call"] is False
    assert a["data_source_restrictions"]["factor_recalculation_executed"] is False
