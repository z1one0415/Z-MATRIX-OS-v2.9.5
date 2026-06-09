"""Tests for V13.F5.5.4.2 Blocked Source Repair Plan."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_4_2_blocked_source_repair_plan")
def _l(n): return json.loads((D / n).read_text())

def test_all_artifacts_exist():
    assert (D / "v13_f5_5_4_2_blocked_source_repair_contract.json").exists()
    assert (D / "v13_f5_5_4_2_f14_f15_f16_source_gap_audit.json").exists()
    assert (D / "v13_f5_5_4_2_required_data_contract.json").exists()
    assert (D / "v13_f5_5_4_2_repair_plan_closeout.json").exists()

def test_contract():
    c = _l("v13_f5_5_4_2_blocked_source_repair_contract.json")
    assert c["planning_only"] is True
    assert c["target_factors"] == ["F14", "F15", "F16"]
    assert c["price_proxy_substitution_allowed"] is False
    assert c["signal_score_generation_allowed"] is False

def test_source_gap():
    g = _l("v13_f5_5_4_2_f14_f15_f16_source_gap_audit.json")
    for fid in ["F14", "F15", "F16"]:
        assert fid in g["factor_gaps"]
        gap = g["factor_gaps"][fid]
        assert gap["available_data"] == []
        assert len(gap["repair_options"]) >= 1
    assert g["factor_gaps"]["F14"]["price_proxy_allowed"] is False
    assert g["factor_gaps"]["F15"]["synthetic_fundamentals_allowed"] is False
    assert g["factor_gaps"]["F16"]["price_proxy_allowed"] is False

def test_required_data():
    r = _l("v13_f5_5_4_2_required_data_contract.json")
    pit = r["F14_F15_requirements"]["pit_rules"]
    assert pit["must_use_ann_date_not_report_period"] is True
    assert pit["must_not_forward_fill_future_data"] is True
    assert pit["must_not_use_synthetic_fundamentals"] is True

def test_closeout():
    co = _l("v13_f5_5_4_2_repair_plan_closeout.json")
    assert co["planning_only"] is True
    assert co["repair_executed"] is False
    assert co["signal_scores_generated"] is False
    assert co["production"] == "BLOCKED"
