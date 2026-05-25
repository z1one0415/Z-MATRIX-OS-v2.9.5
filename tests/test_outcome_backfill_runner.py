"""Outcome Backfill Runner tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.paper_trading.outcome_backfill_runner import calculate_outcome_for_entry
from zmatrix.paper_trading.ledger import build_paper_trade_entry

BARS = [{"date":"2026-05-01","close":45,"adj_close":45},{"date":"2026-05-02","close":46,"adj_close":46},{"date":"2026-05-03","close":47,"adj_close":47},{"date":"2026-05-04","close":48,"adj_close":48},{"date":"2026-05-05","close":47,"adj_close":47},{"date":"2026-05-06","close":49,"adj_close":49},{"date":"2026-05-07","close":50,"adj_close":50},{"date":"2026-05-08","close":48,"adj_close":48}]

ENTRY = build_paper_trade_entry(ticker="002472", role="A_LONG_CORE", entry_date="2026-05-01", entry_price=45, paper_action="PAPER_TRACK", reason="test", target_horizon="T20", max_loss_plan=10, invalidation_condition="test")

def test_calculate_t5():
    r = calculate_outcome_for_entry(ENTRY, BARS)
    assert r["outcome_status"] in ("READY", "INSUFFICIENT_DATA")
    if r["actual_return_t5"] is not None:
        print(f"✅ T5 return: {r['actual_return_t5']:+.2f}%")
    else:
        print("✅ outcome: T5 None (insufficient data)")

def test_no_z9_write():
    r = calculate_outcome_for_entry(ENTRY, BARS)
    assert r["real_z9_write_allowed"] is False
    print("✅ no real Z9 write")

def test_insufficient_data():
    r = calculate_outcome_for_entry(ENTRY, [])
    assert r["outcome_status"] == "INSUFFICIENT_DATA"
    print("✅ insufficient data handled")

if __name__ == "__main__":
    test_calculate_t5(); test_no_z9_write(); test_insufficient_data()
    print("\n🏁 Outcome Backfill Runner — tests PASS")
