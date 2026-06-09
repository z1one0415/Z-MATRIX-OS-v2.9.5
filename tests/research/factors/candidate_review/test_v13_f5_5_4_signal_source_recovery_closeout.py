"""Tests for V13.F5.5.4 Signal Source Recovery Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")


def _l(n):
    return json.loads((D / n).read_text())


def test_closeout_exists():
    assert (D / "v13_f5_5_4_signal_source_recovery_closeout.json").exists()


def test_closeout_status():
    co = _l("v13_f5_5_4_signal_source_recovery_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-4-SIGNAL-SOURCE-RECOVERY-CLOSEOUT"
    assert co["status"] == "V13_F5_5_4_SIGNAL_SOURCE_RECOVERY_PASS"


def test_restoration_results():
    co = _l("v13_f5_5_4_signal_source_recovery_closeout.json")
    assert co["source_recovery_executed"] is True
    assert set(co["restored_factors"]) == {"F04", "F10", "F11", "F14", "F15", "F16"}
    assert co["blocked_factors"] == []
    assert set(co["ready_for_signal_materialization"]) == {"F04", "F10", "F11", "F14", "F15", "F16"}


def test_no_execution():
    co = _l("v13_f5_5_4_signal_source_recovery_closeout.json")
    assert co["signal_score_generation_executed"] is False
    assert co["monitoring_rerun_executed"] is False
    assert co["candidate_state_update_executed"] is False


def test_blocked():
    co = _l("v13_f5_5_4_signal_source_recovery_closeout.json")
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
    co = _l("v13_f5_5_4_signal_source_recovery_closeout.json")
    assert co["recommended_next_action"] == "PREPARE_V13_F5_5_4_1_SIGNAL_SCORE_MATERIALIZATION_FOR_RESTORED_BATCH1_BATCH2_FACTORS"
