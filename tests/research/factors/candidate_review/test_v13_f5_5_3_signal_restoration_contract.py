"""Tests for V13.F5.5.3 Signal Restoration Contract."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_contract_exists():
    assert (D / "v13_f5_5_3_signal_restoration_contract.json").exists()


def test_contract_fields():
    c = _l("v13_f5_5_3_signal_restoration_contract.json")
    assert c["pipeline_signature"] == "Z2-V13-F5-5-3-SIGNAL-SCORE-RESTORATION-CONTRACT"
    assert c["status"] == "V13_F5_5_3_SIGNAL_RESTORATION_CONTRACT_BUILT"
    assert c["planning_only"] is True
    assert len(c["frozen_candidates"]) == 10
    assert c["current_signal_available_count"] == 0
    assert c["current_signal_blocked_count"] == 10


def test_contract_no_materialization():
    c = _l("v13_f5_5_3_signal_restoration_contract.json")
    assert c["factor_recalculation_allowed"] is False
    assert c["signal_materialization_allowed"] is False
    assert c["monitoring_rerun_allowed"] is False
    assert c["candidate_state_update_allowed"] is False


def test_contract_blocked():
    c = _l("v13_f5_5_3_signal_restoration_contract.json")
    assert c["promotion_allowed"] is False
    assert c["runner_enabled"] is False
    assert c["execution_allowed"] is False
    assert c["v13_6_allowed"] is False
    assert c["alpha_claim_allowed"] is False
    assert c["production"] == "BLOCKED"
    assert c["broker_runtime"] == "BLOCKED"
    assert c["real_trade"] == "BLOCKED"
