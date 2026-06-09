"""Tests for V13.F5.5.3.1 Signal Coverage Validation."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_validation_exists():
    assert (D / "v13_f5_5_3_1_signal_coverage_validation.json").exists()


def test_coverage_pass():
    v = _l("v13_f5_5_3_1_signal_coverage_validation.json")
    assert v["pipeline_signature"] == "Z2-V13-F5-5-3-1-SIGNAL-COVERAGE-VALIDATION"
    assert v["status"] == "V13_F5_5_3_1_SIGNAL_COVERAGE_PASS"
    assert v["all_eligible_factors_complete"] is True


def test_per_factor_coverage():
    v = _l("v13_f5_5_3_1_signal_coverage_validation.json")
    for fid in ["F21", "F24", "F30", "F31"]:
        fc = v["factor_coverage"][fid]
        assert fc["covered"] == 5
        assert fc["missing"] == []
        assert fc["coverage_complete"] is True


def test_counts():
    v = _l("v13_f5_5_3_1_signal_coverage_validation.json")
    assert v["label_ticker_count"] == 5
    assert v["covered_factor_count"] == 4
    assert v["blocked_factor_count"] == 10
