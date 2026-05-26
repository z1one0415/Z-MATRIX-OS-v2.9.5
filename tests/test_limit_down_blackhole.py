"""LIMIT_DOWN_BLACKHOLE tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.limit_down_blackhole import evaluate_limit_down_blackhole

def test_limit_down_blackhole_triggers_isolation():
    r = evaluate_limit_down_blackhole(market_signals={"limit_down_count": 80})
    assert r["decision"] == "ISOLATE"
    assert r["freeze_new_entries"] is True
    print("✅ blackhole triggers ISOLATE")

def test_limit_down_blackhole_no_real_sell():
    r = evaluate_limit_down_blackhole(market_signals={"limit_down_count": 120})
    assert r["safety"]["auto_sell_allowed"] is False
    print("✅ blackhole no auto sell")

if __name__ == "__main__":
    test_limit_down_blackhole_triggers_isolation()
    test_limit_down_blackhole_no_real_sell()
    print("\n🏁 Limit Down Blackhole tests PASS")
