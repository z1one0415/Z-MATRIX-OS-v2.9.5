"""Lightweight Backtest integration tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.backtest.lightweight_backtest import run_lightweight_role_backtest

def test_backtest_with_entries():
    entries = [{"ticker":"002472","role":"A_LONG_CORE","entry_date":"2026-05-01","entry_price":45},
               {"ticker":"601899","role":"B_MID_ROTATION","entry_date":"2026-05-01","entry_price":30},
               {"ticker":"588000","role":"C_SHORT_EVENT","entry_date":"2026-05-01","entry_price":2}]
    bars = {}
    for t, base in [("002472",45),("601899",30),("588000",2)]:
        bars[t] = [{"date":f"2026-05-{d:02d}","close":base+i*0.3,"adj_close":base+i*0.3} for i,d in enumerate(range(1,30))]
    r = run_lightweight_role_backtest(entries, bars)
    assert r["ALL"]["count"] == 3
    for role in ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","ALL"]:
        assert role in r
    print(f"✅ backtest: {r['ALL']['count']} entries, roles={[k for k in r.keys() if k != 'ALL']}")

if __name__ == "__main__":
    test_backtest_with_entries()
    print("\n🏁 Lightweight Backtest — tests PASS")
