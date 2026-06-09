"""Tests for V13.F5.5.2.2 Seven-Factor Partial Monitoring Contract."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
def _l(n): return json.loads((D / n).read_text())

def test_contract_exists():
    assert (D / "v13_f5_5_2_2_seven_factor_partial_monitoring_contract.json").exists()

def test_contract_scope():
    c = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_contract.json")
    assert c["monitoring_scope"] == ["F04", "F10", "F11", "F21", "F24", "F30", "F31"]
    assert c["blocked_factors"] == ["F14", "F15", "F16"]
    assert c["ticker_count"] == 5
    assert c["expected_signal_rows"] == 35
    assert c["sample_scope"] == "MICRO_SAMPLE_5_TICKERS"

def test_contract_no_formal():
    c = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_contract.json")
    assert c["formal_oos_validation_allowed"] is False
    assert c["formal_statistical_inference_allowed"] is False
    assert c["candidate_state_update_allowed"] is False
    assert c["promotion_allowed"] is False

def test_contract_blocked():
    c = _l("v13_f5_5_2_2_seven_factor_partial_monitoring_contract.json")
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
