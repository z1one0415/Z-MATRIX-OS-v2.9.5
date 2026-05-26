"""DOMESTIC_LIQUIDITY_CRASH tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.domestic_liquidity_crash import evaluate_domestic_liquidity_crash

def test_domestic_liquidity_crash_freezes_d_matrix():
    r = evaluate_domestic_liquidity_crash(market_signals={"liquidity_scissor": 0.60, "small_cap_liquidity_score": 0.20})
    assert r["decision"] == "FREEZE"
    assert "D_BLACK_HORSE" in r["affected_roles"]
    print("✅ liquidity crash freezes D-Matrix")

if __name__ == "__main__":
    test_domestic_liquidity_crash_freezes_d_matrix()
    print("\n🏁 Domestic Liquidity Crash tests PASS")
