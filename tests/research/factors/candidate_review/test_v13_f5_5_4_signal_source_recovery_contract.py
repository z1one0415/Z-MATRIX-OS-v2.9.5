"""Tests for V13.F5.5.4 Signal Source Recovery Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")


def _l(n):
    return json.loads((D / n).read_text())


def test_contract_exists():
    assert (D / "v13_f5_5_4_signal_source_recovery_contract.json").exists()


def test_contract_fields():
    c = _l("v13_f5_5_4_signal_source_recovery_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-4-SIGNAL-SOURCE-RECOVERY-CONTRACT"
    assert c["planning_and_restoration_only"] is True
    assert c["target_factors"] == ["F04", "F10", "F11", "F14", "F15", "F16"]
    assert c["already_signal_ready"] == ["F21", "F24", "F30", "F31"]
    assert c["signal_score_generation_allowed"] is False
    assert c["monitoring_rerun_allowed"] is False


def test_contract_blocked():
    c = _l("v13_f5_5_4_signal_source_recovery_contract.json")
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
