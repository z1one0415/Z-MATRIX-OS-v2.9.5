#!/usr/bin/env python3
"""Pack C.4.1: Complete Blocking Fix Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent

def test_risk_register_no_blocking():
    data = json.loads((WORKSPACE / "runtime_reports" / "audit" / "core_module_risk_register.json").read_text())
    blocking = [r for r in data if r.get("blocking_pack_d")]
    assert len(blocking) == 0, f"Still blocking: {blocking}"

# ── account_truth: wire check ──
def test_reconcile_trade_amount_uses_tolerance():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_trade_amount
    from zmatrix.research_db.account_truth import TradeRecord
    t = TradeRecord(trade_id="T1", ticker="X", trade_date="D", side="BUY", price=10, quantity=100, amount=1001)
    r = reconcile_trade_amount(t, strict_mode=True)
    assert r["status"] == "ERROR"  # 1000 vs 1001, strict → ERROR
    assert "difference_abs" in r
    assert "tolerance_abs" in r

def test_reconcile_equity_uses_tolerance():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_equity
    from zmatrix.research_db.account_truth import AccountSnapshot
    s = AccountSnapshot(date="D", total_equity=100000, cash=50000, market_value=50000)
    r = reconcile_equity(s)
    assert r["status"] == "PASS"
    assert "difference_abs" in r

def test_reconcile_equity_big_mismatch():
    from zmatrix.research_db.account_truth.account_reconciler import reconcile_equity
    from zmatrix.research_db.account_truth import AccountSnapshot
    s = AccountSnapshot(date="D", total_equity=100000, cash=30000, market_value=50000)
    r = reconcile_equity(s, strict_mode=True)
    assert r["status"] == "ERROR"

# ── replay: fail-closed check ──
def test_rolling_dataset_calendar_none_raises():
    from zmatrix.research_db.replay.replay_dataset import RollingDataset
    import pytest
    ds = RollingDataset(tickers=["A"])
    with pytest.raises(ValueError, match="MISSING_TRADING_CALENDAR"):
        ds.generate_rolling_slices("2024-01-02", "2024-01-09")

def test_rolling_runner_calendar_none_fail_closed():
    from zmatrix.research_db.replay.replay_dataset import ReplayDataset
    from zmatrix.research_db.replay.replay_runner import ReplayRunner
    ds = ReplayDataset(tickers=["A"])
    runner = ReplayRunner(ds)
    r = runner.run_rolling_replay("E1", "2024-01-02", "2024-01-09")
    assert r.status in ("FAILED", "ERROR"), f"Expected FAILED: {r.status}"
    assert "CALENDAR" in r.details.get("error_type", "").upper()

def test_closeout_exists(): assert (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C4_1_CLOSEOUT.md").exists()
def test_c4_1_status(): 
    text = (WORKSPACE / "docs" / "audit" / "MAJOR_AUDIT_PACK_C4_1_CLOSEOUT.md").read_text()
    assert "PACK_C4_1_FIX_COMPLETE" in text

if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
