"""Tests for V13.F5.5.1.2 Actual Label Horizon Completeness."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_validation_exists():
    assert (D / "v13_f5_5_1_2_actual_label_horizon_completeness.json").exists()


def test_validation_pass():
    v = _l("v13_f5_5_1_2_actual_label_horizon_completeness.json")
    assert v["pipeline_signature"] == "Z2-V13-F5-5-1-2-ACTUAL-LABEL-HORIZON-COMPLETENESS"
    assert v["status"] == "V13_F5_5_1_2_HORIZON_COMPLETENESS_PASS"


def test_horizon_results():
    v = _l("v13_f5_5_1_2_actual_label_horizon_completeness.json")
    assert v["results"]["5D"] == "PASS"
    assert v["results"]["20D"] == "PASS"
    assert v["results"]["60D"] == "BLOCKED_NOT_GENERATED"


def test_horizon_counts():
    v = _l("v13_f5_5_1_2_actual_label_horizon_completeness.json")
    assert v["counts"]["5D"] > 0
    assert v["counts"]["20D"] > 0
    assert v["counts"]["60D"] == 0
