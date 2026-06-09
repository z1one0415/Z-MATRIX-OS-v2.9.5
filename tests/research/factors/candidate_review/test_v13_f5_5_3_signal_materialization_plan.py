"""Tests for V13.F5.5.3 Signal Materialization Plan."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_plan_exists():
    assert (D / "v13_f5_5_3_signal_materialization_plan.json").exists()


def test_plan_status():
    p = _l("v13_f5_5_3_signal_materialization_plan.json")
    assert p["pipeline_signature"] == "Z2-V13-F5-5-3-SIGNAL-MATERIALIZATION-PLAN"
    assert p["status"] == "V13_F5_5_3_SIGNAL_MATERIALIZATION_PLAN_BUILT"


def test_two_step_plan():
    p = _l("v13_f5_5_3_signal_materialization_plan.json")
    assert p["f5_5_3_scope"] == "PLAN_AND_AUDIT_ONLY"
    assert p["f5_5_3_1_scope"] == "MATERIALIZE_SIGNAL_SCORES_FOR_LABEL_TICKERS_ONLY"


def test_eligible_factors():
    p = _l("v13_f5_5_3_signal_materialization_plan.json")
    assert len(p["f5_5_3_1_eligible_factors"]) == 4
    assert set(p["f5_5_3_1_eligible_factors"]) == {"F21", "F24", "F30", "F31"}


def test_f5_5_3_1_constraints():
    p = _l("v13_f5_5_3_signal_materialization_plan.json")
    c = p["f5_5_3_1_constraints"]
    assert c["only_for_label_tickers"] is True
    assert c["only_for_rebalance_date"] is True
    assert c["no_full_universe_computation"] is True
    assert c["no_feature_store_write"] is True
    assert c["no_runtime_reports_write"] is True
    assert c["no_candidate_state_update"] is True
    assert c["no_trade_signal_output"] is True
    assert c["no_alpha_claim"] is True


def test_no_execution_in_f5_5_3():
    p = _l("v13_f5_5_3_signal_materialization_plan.json")
    assert p["signal_materialization_executed_in_f5_5_3"] is False
    assert p["factor_recalculation_executed"] is False
    assert p["monitoring_rerun_executed"] is False
    assert p["candidate_state_update_executed"] is False


def test_blocked():
    p = _l("v13_f5_5_3_signal_materialization_plan.json")
    assert p["promotion_allowed"] is False
    assert p["runner_enabled"] is False
    assert p["execution_allowed"] is False
    assert p["production"] == "BLOCKED"
    assert p["broker_runtime"] == "BLOCKED"
    assert p["real_trade"] == "BLOCKED"
