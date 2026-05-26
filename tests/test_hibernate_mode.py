"""HIBERNATE_MODE tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.hibernate_mode import evaluate_hibernate_mode

def test_hibernate_mode_when_hard_gate_pass_rate_below_1pct():
    r = evaluate_hibernate_mode(market_signals={"hard_gate_pass_rate": 0.005})
    assert r["decision"] == "HIBERNATE"
    assert r["freeze_new_entries"] is True
    print("✅ hibernate on <1% pass rate")

if __name__ == "__main__":
    test_hibernate_mode_when_hard_gate_pass_rate_below_1pct()
    print("\n🏁 Hibernate Mode tests PASS")
