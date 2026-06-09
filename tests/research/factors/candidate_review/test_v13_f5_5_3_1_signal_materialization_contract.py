"""Tests for V13.F5.5.3.1 Signal Materialization Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_contract_exists():
    assert (D / "v13_f5_5_3_1_signal_materialization_contract.json").exists()


def test_contract_scope():
    c = _l("v13_f5_5_3_1_signal_materialization_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-3-1-SIGNAL-MATERIALIZATION-CONTRACT"
    assert c["materialization_scope"] == "MINIMAL_LABEL_TICKERS_ONLY"
    assert c["eligible_factors"] == ["F21", "F24", "F30", "F31"]
    assert c["rebalance_date"] == "2026-05-06"
    assert c["label_tickers_only"] is True
    assert c["full_universe_computation_allowed"] is False


def test_contract_blocked():
    c = _l("v13_f5_5_3_1_signal_materialization_contract.json")
    assert c["feature_store_write_allowed"] is False
    assert c["runtime_reports_write_allowed"] is False
    assert c["monitoring_rerun_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
