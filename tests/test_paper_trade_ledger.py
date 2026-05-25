"""Paper Trade Ledger tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.paper_trading.ledger import build_paper_trade_entry

def test_build_entry():
    e = build_paper_trade_entry(ticker="002472", role="A_LONG_CORE", entry_date="2026-05-01", entry_price=45, paper_action="PAPER_TRACK", reason="long-term base", target_horizon="T20", max_loss_plan=10, invalidation_condition="业绩miss")
    assert e["role"] == "A_LONG_CORE"
    assert e["paper_id"] is not None
    assert len(e["paper_id"]) == 32
    assert e["real_trade_allowed"] is False
    print(f"✅ paper ledger entry: {e['ticker']} role={e['role']} id={e['paper_id'][:8]}...")

def test_reject_reject_role():
    try:
        build_paper_trade_entry(ticker="002472", role="D_REJECT", entry_date="2026-05-01", entry_price=40, paper_action="PAPER_TRACK", reason="test", target_horizon="T20", max_loss_plan=5, invalidation_condition="none")
        assert False, "should reject D_REJECT"
    except ValueError as e: assert "D_REJECT" in str(e)
    print("✅ D_REJECT rejected")

def test_watch_only_reject():
    try:
        build_paper_trade_entry(ticker="002472", role="WATCH_ONLY", entry_date="2026-05-01", entry_price=40, paper_action="PAPER_TRACK", reason="test", target_horizon="T20", max_loss_plan=5, invalidation_condition="none")
        assert False, "should reject WATCH_ONLY"
    except ValueError: pass
    print("✅ WATCH_ONLY rejected")

def test_forbidden_action():
    try:
        build_paper_trade_entry(ticker="002472", role="A_LONG_CORE", entry_date="2026-05-01", entry_price=40, paper_action="BUY", reason="test", target_horizon="T20", max_loss_plan=5, invalidation_condition="none")
        assert False, "should reject BUY"
    except ValueError as e: assert "BUY" in str(e)
    print("✅ BUY rejected")

if __name__ == "__main__":
    test_build_entry(); test_reject_reject_role(); test_watch_only_reject(); test_forbidden_action()
    print("\n🏁 Paper Trade Ledger — tests PASS")
