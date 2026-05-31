import json
from pathlib import Path
import pytest
W = Path(__file__).resolve().parent.parent.parent
@pytest.fixture
def closeout():
    p = W / "runtime_reports" / "cases" / "case_expansion_v5_closeout.json"
    if not p.exists(): pytest.skip("Closeout not yet generated")
    return json.loads(p.read_text())
def test_closeout_status(closeout):
    assert "CONFIRMED" in closeout["status"]
def test_v5_entry_allowed(closeout):
    assert closeout["v5_entry_allowed"] is True
def test_zero_alpha(closeout):
    assert closeout["predictive_alpha_claim_count"] == 0
def test_zero_bs(closeout):
    assert closeout["buy_sell_instruction_count"] == 0
def test_blocked(closeout):
    assert closeout["production"] == "BLOCKED"
    assert closeout["broker_runtime"] == "BLOCKED"
    assert closeout["real_trade"] == "BLOCKED"
def test_council_blocked(closeout):
    assert "BLOCKED" in closeout["council_investment_verdict"]
