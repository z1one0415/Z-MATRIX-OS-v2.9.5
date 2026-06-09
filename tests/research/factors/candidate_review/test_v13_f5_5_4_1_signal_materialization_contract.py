"""Tests for V13.F5.5.4.1 Signal Materialization Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")

def _l(n): return json.loads((D / n).read_text())

def test_contract_exists():
    assert (D / "v13_f5_5_4_1_signal_materialization_contract.json").exists()

def test_contract_fields():
    c = _l("v13_f5_5_4_1_signal_materialization_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-4-1-BATCH1-BATCH2-SIGNAL-MATERIALIZATION-CONTRACT"
    assert c["target_factors"] == ["F04", "F10", "F11", "F14", "F15", "F16"]
    assert c["already_signal_ready"] == ["F21", "F24", "F30", "F31"]
    assert c["materialization_scope"] == "MINIMAL_LABEL_TICKERS_ONLY"
    assert c["full_universe_computation_allowed"] is False

def test_contract_blocked():
    c = _l("v13_f5_5_4_1_signal_materialization_contract.json")
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
