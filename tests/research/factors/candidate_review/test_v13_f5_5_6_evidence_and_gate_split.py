"""Tests for V13.F5.5.6 Evidence Limitations, Gate Split, G18 Handoff."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
def _l(n): return json.loads((D / n).read_text())

def test_evidence_limitations():
    a = _l("v13_f5_5_6_current_evidence_limitation_audit.json")
    assert a["current_evidence"]["ticker_count"] == 5
    assert a["current_evidence"]["label_month_count"] == 1
    assert a["current_evidence"]["signal_ready_factors"] == 7
    assert a["formal_gates"]["formal_oos_validation_allowed"] is False

def test_prohibitions():
    a = _l("v13_f5_5_6_current_evidence_limitation_audit.json")
    assert a["prohibitions"]["F10_positive_spread_is_NOT_alpha_claim"] is True
    assert a["prohibitions"]["negative_spread_is_NOT_rejection_signal"] is True
    assert a["prohibitions"]["no_promotion_from_micro_sample"] is True

def test_gate_split():
    s = _l("v13_f5_5_6_seven_vs_ten_factor_gate_split.json")
    assert s["seven_factor_path"]["can_enter_expanded_diagnostic"] is True
    assert s["seven_factor_path"]["promotion_allowed"] is False
    assert s["ten_factor_path"]["blocked_until_f14_f15_f16_repaired"] is True

def test_blocked_factor_rules():
    s = _l("v13_f5_5_6_seven_vs_ten_factor_gate_split.json")
    assert s["blocked_factor_rules"]["F14_F15_F16_not_downgraded_due_to_missing_source"] is True
    assert s["blocked_factor_rules"]["F14_F15_F16_not_replaced_by_price_proxy"] is True

def test_g18_handoff():
    g = _l("v13_f5_5_6_g18_handoff_gate_plan.json")
    assert g["current_factor_monitoring_use_for_g18"] == "OBSERVATION_ONLY"
    assert g["auto_weight_update_allowed"] is False
    assert g["micro_sample_result_not_allowed_for_g18_reweighting"] is True
    assert g["minimum_requirement_for_g18_reweighting"]["oos_months"] == 6
