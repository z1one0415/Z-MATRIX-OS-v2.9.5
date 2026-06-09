"""Tests for V13.F5.5.3 Signal Source Classification."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_classification_exists():
    assert (D / "v13_f5_5_3_signal_source_classification.json").exists()


def test_classification_status():
    c = _l("v13_f5_5_3_signal_source_classification.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-3-SIGNAL-SOURCE-CLASSIFICATION"
    assert c["status"] == "V13_F5_5_3_SIGNAL_SOURCE_CLASSIFICATION_COMPLETE"


def test_summary():
    c = _l("v13_f5_5_3_signal_source_classification.json")
    s = c["summary"]
    assert s["total_frozen_candidates"] == 10
    assert s["actionable_for_f5_5_3_1"] == 4
    assert s["blocked_requires_prior_work"] == 6


def test_eligible_factors():
    c = _l("v13_f5_5_3_signal_source_classification.json")
    eligible = c["f5_5_3_1_eligible_factors"]
    assert set(eligible) == {"F21", "F24", "F30", "F31"}


def test_blocked_factors():
    c = _l("v13_f5_5_3_signal_source_classification.json")
    blocked = c["blocked_factors_requiring_prior_batch_work"]
    assert set(blocked) == {"F04", "F10", "F11", "F14", "F15", "F16"}


def test_all_paths_classified():
    c = _l("v13_f5_5_3_signal_source_classification.json")
    assert len(c["factor_restoration_paths"]) == 10
    for p in c["factor_restoration_paths"]:
        assert "restoration_class" in p
        assert "actionable_in_f5_5_3_1" in p
