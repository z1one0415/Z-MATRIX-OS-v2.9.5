"""Test V4 closeout."""
import json
from pathlib import Path
import pytest

WORKSPACE = Path(__file__).resolve().parent.parent.parent

@pytest.fixture
def closeout():
    p = WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v4_closeout.json"
    return json.loads(p.read_text()) if p.exists() else None

def test_v4_closeout_exists(closeout):
    assert closeout is not None, "Closeout not generated"

def test_v4_closeout_status(closeout):
    assert "CASE_EXPANSION_V4" in closeout["status"]

def test_v4_core_12(closeout):
    assert closeout["core_12_cases"] == 12

def test_v4_no_alpha(closeout):
    assert closeout["ready_for_alpha_claim"] == 0

def test_v4_no_buy_sell(closeout):
    assert closeout["buy_sell_instruction_count"] == 0

def test_v4_production_blocked(closeout):
    assert closeout["production"] == "BLOCKED"

def test_v4_broker_blocked(closeout):
    assert closeout["broker_runtime"] == "BLOCKED"

def test_v4_real_trade_blocked(closeout):
    assert closeout["real_trade"] == "BLOCKED"

def test_v4_honesty():
    """If no real data, status must not claim CONFIRMED — use PARTIAL or BLOCKED."""
    # Get actual data readiness
    rd = json.loads((WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json").read_text())
    has_real_data = rd["summary"]["daily_price_real"] > 0
    if not has_real_data:
        # Without real data, status should not claim full CONFIRMED
        closeout = json.loads((WORKSPACE / "runtime_reports" / "cases" / "case_expansion_v4_closeout.json").read_text())
    assert "CONFIRMED" not in closeout["status"].upper() or "PARTIAL" in closeout["status"].upper() or "BLOCKED" in closeout["status"].upper(), \
            f"Status {closeout['status']} claims CONFIRMED but no real data exists"
