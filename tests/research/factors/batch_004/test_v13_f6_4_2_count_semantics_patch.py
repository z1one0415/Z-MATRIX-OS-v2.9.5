"""Test V13.F6.4.2 Count Semantics Patch."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def test_patch_exists():
    assert (D / "v13_f6_4_2_count_semantics_patch.json").exists()

def test_informative_count():
    p = _l("v13_f6_4_2_count_semantics_patch.json")
    c = p["corrected_counts"]
    assert c["informative_signal_ready"] == 23
    assert c["materialized_signal_ready"] == 24
    assert c["materialized_non_informative"] == ["F13"]

def test_rejected_count():
    p = _l("v13_f6_4_2_count_semantics_patch.json")
    assert p["corrected_counts"]["rejected"] == 3

def test_patches_listed():
    p = _l("v13_f6_4_2_count_semantics_patch.json")
    fixes = p["patch_from_f6_4_1"]
    assert "f02_f03_f05" in fixes
    assert "f01" in fixes
    assert "f17_f20" in fixes
    assert "f13" in fixes
    assert "f03r" in fixes

def test_alpha_zero():
    p = _l("v13_f6_4_2_count_semantics_patch.json")
    assert p["corrected_counts"]["formal_alpha_factor_count"] == 0
