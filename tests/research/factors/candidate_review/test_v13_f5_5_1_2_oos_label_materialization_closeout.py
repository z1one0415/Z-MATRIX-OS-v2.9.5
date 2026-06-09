"""Tests for V13.F5.5.1.2 OOS Label Materialization Closeout."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_closeout_exists():
    assert (D / "v13_f5_5_1_2_oos_label_materialization_closeout.json").exists()


def test_closeout_status():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["pipeline_signature"] == "Z2-V13-F5-5-1-2-OOS-LABEL-MATERIALIZATION-CLOSEOUT"
    assert co["status"] == "V13_F5_5_1_2_OOS_LABEL_MATERIALIZATION_PASS"


def test_label_generation():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["read_only_price_data_access_used"] is True
    assert co["label_month"] == "2026-05"
    assert co["generated_horizons"] == ["5D", "20D"]
    assert co["blocked_horizons"] == ["60D"]
    assert co["actual_forward_returns_generated"] is True
    assert co["label_data_row_count"] > 0
    assert co["label_role"] == "OUTCOME_LABEL_ONLY"


def test_isolation():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["written_to_feature_store"] is False
    assert co["used_for_factor_calculation"] is False
    assert co["used_for_candidate_decision"] is False
    assert co["used_for_monitoring_execution"] is False


def test_no_execution():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["monitoring_execution_executed"] is False
    assert co["true_oos_validation_executed"] is False
    assert co["candidate_decision_update_executed"] is False


def test_monitoring_ready():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["ready_for_first_monitoring_execution"] is True
    assert co["ready_for_promotion_review"] == []
    assert co["promotion_allowed"] is False


def test_blocked():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["runner_enabled"] is False
    assert co["execution_allowed"] is False
    assert co["v13_6_allowed"] is False
    assert co["paper_trading_allowed"] is False
    assert co["alpha_claim_allowed"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


def test_next_action():
    co = _l("v13_f5_5_1_2_oos_label_materialization_closeout.json")
    assert co["recommended_next_action"] == "EXECUTE_V13_F5_5_2_FIRST_PARTIAL_MONITORING_EXECUTION"
