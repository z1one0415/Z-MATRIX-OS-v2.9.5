"""Tests for V13.F5.5.4.1 Signal Coverage Validation."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")

def _l(n): return json.loads((D / n).read_text())

def test_coverage_partial():
    v = _l("v13_f5_5_4_1_signal_coverage_validation.json")
    assert v["status"] == "V13_F5_5_4_1_SIGNAL_COVERAGE_PARTIAL"

def test_price_based_pass():
    v = _l("v13_f5_5_4_1_signal_coverage_validation.json")
    for fid in ["F04", "F10", "F11"]:
        assert v["factor_coverage"][fid]["status"] == "PASS"
        assert v["factor_coverage"][fid]["covered_ticker_count"] == 5
        assert v["factor_coverage"][fid]["rows"] == 5

def test_fundamental_blocked():
    v = _l("v13_f5_5_4_1_signal_coverage_validation.json")
    for fid in ["F14", "F15", "F16"]:
        assert "BLOCKED" in v["factor_coverage"][fid]["status"]
        assert v["factor_coverage"][fid]["rows"] == 0

def test_summary():
    v = _l("v13_f5_5_4_1_signal_coverage_validation.json")
    assert v["summary"]["factors_materialized"] == 3
    assert v["summary"]["factors_blocked"] == 3
    assert v["summary"]["price_based_all_pass"] is True
