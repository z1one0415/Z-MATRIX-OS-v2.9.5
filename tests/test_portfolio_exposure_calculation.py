"""Portfolio Exposure Calculation tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.portfolio_exposure_calculation import calculate_exposure_from_price_history

def _make_bars(n, base=40): return [{"date":f"2026-01-{d:02d}"if d<32 else f"2026-02-{d-31:02d}","close":base+i*0.5,"adj_close":base+i*0.5} for i,d in enumerate(range(1,n+1))]

def test_degraded_on_insufficient():
    r=calculate_exposure_from_price_history({"ticker":"002472","chain":"ROBOT"},[],{"002472":_make_bars(5)})
    assert r["degraded"]; assert not r["exposure_gate_passed"]; assert not r["add_position_allowed"]
    print("✅ degraded on insufficient")

def test_sufficient():
    b=_make_bars(250); r=calculate_exposure_from_price_history({"ticker":"T"},[],{"T":b},market_proxy_bars=b)
    assert not r["degraded"]; print(f"✅ not degraded (beta={r['market_beta']})")

def test_chain_exposure_blocks_add_position():
    b=_make_bars(250)
    r=calculate_exposure_from_price_history({"ticker":"002472","chain":"ROBOT","proposed_weight":8},[{"ticker":"300001","chain":"ROBOT","weight":30}],{"002472":b,"300001":b},market_proxy_bars=b)
    assert r["duplicate_exposure_pct"]==38.0; assert not r["exposure_gate_passed"]; assert not r["add_position_allowed"]
    assert "CHAIN_EXPOSURE" in str(r["warnings"]); print(f"✅ chain exposure blocked (dup={r['duplicate_exposure_pct']}%)")

def test_low_exposure_allowed():
    b=_make_bars(250)
    r=calculate_exposure_from_price_history({"ticker":"002472","chain":"ROBOT","proposed_weight":5},[{"ticker":"300001","chain":"ROBOT","weight":10}],{"002472":b,"300001":b},market_proxy_bars=b)
    assert r["exposure_gate_passed"]; assert r["add_position_allowed"]
    print(f"✅ low exposure allowed (dup={r['duplicate_exposure_pct']}%)")

if __name__ == "__main__":
    test_degraded_on_insufficient(); test_sufficient()
    test_chain_exposure_blocks_add_position(); test_low_exposure_allowed()
    print("\n🏁 Portfolio Exposure Calculation — tests PASS")
