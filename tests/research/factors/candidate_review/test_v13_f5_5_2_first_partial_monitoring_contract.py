"""Tests for V13.F5.5.2 First Partial Monitoring Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")


def _l(n):
    return json.loads((D / n).read_text())


def test_contract_exists():
    assert (D / "v13_f5_5_2_first_partial_monitoring_contract.json").exists()


def test_contract_scope():
    c = _l("v13_f5_5_2_first_partial_monitoring_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-2-FIRST-PARTIAL-MONITORING-CONTRACT"
    assert c["status"] == "V13_F5_5_2_FIRST_PARTIAL_MONITORING_CONTRACT_BUILT"
    assert c["monitoring_execution_scope"] == "MICRO_SAMPLE_PARTIAL_DIAGNOSTIC_ONLY"
    assert c["label_month"] == "2026-05"
    assert c["allowed_horizons"] == ["5D", "20D"]
    assert c["blocked_horizons"] == ["60D"]
    assert len(c["monitoring_scope"]) == 10


def test_contract_no_formal_validation():
    c = _l("v13_f5_5_2_first_partial_monitoring_contract.json")
    assert c["formal_oos_validation_allowed"] is False
    assert c["candidate_state_update_allowed"] is False
    assert c["suspension_decision_allowed"] is False
    assert c["rejection_decision_allowed"] is False
    assert c["promotion_allowed"] is False


def test_contract_blocked():
    c = _l("v13_f5_5_2_first_partial_monitoring_contract.json")
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["v13_6_allowed"] is False
    assert c["paper_trading_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
