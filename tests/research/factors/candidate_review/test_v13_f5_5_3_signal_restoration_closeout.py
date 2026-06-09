"""Tests for V13.F5.5.3 Signal Restoration Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_closeout_exists():
    assert (D / "v13_f5_5_3_signal_restoration_closeout.json").exists()


def test_closeout_status():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-3-SIGNAL-SCORE-RESTORATION-CLOSEOUT"
    assert co["status"] == "V13_F5_5_3_SIGNAL_SCORE_RESTORATION_PLAN_PASS"


def test_planning_only():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["planning_only"] is True
    assert co["current_signal_available_count"] == 0
    assert co["current_signal_blocked_count"] == 10


def test_actionable_classification():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["factors_actionable_for_materialization"] == 4
    assert co["factors_blocked_no_source"] == 6
    assert set(co["f5_5_3_1_eligible_factors"]) == {"F21", "F24", "F30", "F31"}


def test_no_execution():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["signal_materialization_executed"] is False
    assert co["factor_recalculation_executed"] is False
    assert co["monitoring_rerun_executed"] is False
    assert co["candidate_state_update_executed"] is False


def test_readiness():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["ready_for_f5_5_3_1_signal_score_materialization"] is True
    assert co["ready_for_f5_5_2_rerun"] is False
    assert co["restoration_plan_built"] is True


def test_blocked():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["ready_for_promotion_review"] == []
    assert co["promotion_allowed"] is False
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["v13_6_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


def test_next_action():
    co = _l("v13_f5_5_3_signal_restoration_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_3_1_MINIMAL_SIGNAL_SCORE_MATERIALIZATION_FOR_EXISTING_LABEL_TICKERS"
