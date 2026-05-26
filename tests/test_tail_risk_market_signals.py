"""Tail-Risk Market Signals tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.market_signals import normalize_market_signals

def test_market_signals_no_external_api():
    raw = {"market_breadth_pass_rate": 0.5, "hard_gate_pass_rate": 0.03}
    sig = normalize_market_signals(raw)
    assert sig["external_api_used"] is False
    assert sig["real_market_fetch_allowed"] is False
    print("✅ market signals no external API")

if __name__ == "__main__":
    test_market_signals_no_external_api()
    print("\n🏁 Market Signals tests PASS")
