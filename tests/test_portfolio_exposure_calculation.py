"""Portfolio Exposure Calculation tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.portfolio_exposure_calculation import calculate_exposure_from_price_history

BARS = { "002472": [{"date":f"2026-{m:02d}-{d:02d}","close":40+i*0.5,"adj_close":40+i*0.5} for i in range(250) for m,d in [(1,1)][:1]] }

def _make_bars(n, base=40):
    return [{"date":f"2026-01-{d:02d}"if d<32 else f"2026-02-{d-31:02d}","close":base+i*0.5,"adj_close":base+i*0.5} for i,d in enumerate(range(1,n+1))]

def test_degraded_on_insufficient():
    r = calculate_exposure_from_price_history({"ticker":"002472","chain":"ROBOT"}, [], {"002472": _make_bars(5)})
    assert r["degraded"] is True
    assert r["exposure_gate_passed"] is False
    assert "INSUFFICIENT_PRICE_HISTORY" in str(r["warnings"])
    print("✅ exposure calc: degraded on insufficient history")

def test_sufficient_data():
    bars = _make_bars(250)
    r = calculate_exposure_from_price_history({"ticker":"002472"}, [], {"002472": bars}, market_proxy_bars=bars)
    assert r["degraded"] is False
    print(f"✅ exposure calc: not degraded (market_beta={r['market_beta']}, max_dd={r['max_drawdown']})")

if __name__ == "__main__":
    test_degraded_on_insufficient(); test_sufficient_data()
    print("\n🏁 Portfolio Exposure Calculation — tests PASS")
