"""Tests for V13.F5.5.1.2 Data Access Authorization Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_contract_exists():
    assert (D / "v13_f5_5_1_2_data_access_authorization_contract.json").exists()


def test_contract_fields():
    c = _l("v13_f5_5_1_2_data_access_authorization_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-1-2-DATA-ACCESS-AUTHORIZATION-CONTRACT"
    assert c["status"] == "V13_F5_5_1_2_DATA_ACCESS_AUTHORIZATION_CONTRACT_BUILT"
    assert c["read_only_price_data_access_requested"] is True
    assert c["read_only_price_data_access_allowed"] is True
    assert c["allowed_source"] == "data/price_bars"
    assert c["allowed_label_month"] == "2026-05"
    assert c["allowed_horizons"] == ["5D", "20D"]
    assert c["blocked_horizons"] == ["60D"]


def test_contract_safety():
    c = _l("v13_f5_5_1_2_data_access_authorization_contract.json")
    assert c["feature_store_write_allowed"] is False
    assert c["monitoring_execution_allowed"] is False
    assert c["candidate_decision_update_allowed"] is False
    assert c["promotion_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["v13_6_allowed"] is False
    assert c["paper_trading_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
