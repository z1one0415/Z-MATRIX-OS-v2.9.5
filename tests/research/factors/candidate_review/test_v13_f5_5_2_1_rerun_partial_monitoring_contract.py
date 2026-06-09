"""Tests for V13.F5.5.2.1 Rerun Partial Monitoring Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_contract_exists():
    assert (D / "v13_f5_5_2_1_rerun_partial_monitoring_contract.json").exists()


def test_contract_scope():
    c = _l("v13_f5_5_2_1_rerun_partial_monitoring_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-2-1-RERUN-PARTIAL-MONITORING-CONTRACT"
    assert c["rerun_scope"] == "FOUR_SIGNAL_READY_FACTORS_MICRO_SAMPLE_ONLY"
    assert c["signal_ready_factors"] == ["F21", "F24", "F30", "F31"]
    assert c["ticker_count"] == 5
    assert c["allowed_horizons"] == ["5D", "20D"]


def test_contract_no_formal():
    c = _l("v13_f5_5_2_1_rerun_partial_monitoring_contract.json")
    assert c["formal_oos_validation_allowed"] is False
    assert c["formal_statistical_inference_allowed"] is False
    assert c["candidate_state_update_allowed"] is False
    assert c["suspension_decision_allowed"] is False
    assert c["rejection_decision_allowed"] is False
    assert c["promotion_allowed"] is False


def test_contract_blocked():
    c = _l("v13_f5_5_2_1_rerun_partial_monitoring_contract.json")
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
