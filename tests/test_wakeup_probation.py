"""WAKEUP_PROBATION tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.wakeup_probation import evaluate_wakeup_probation

def test_wakeup_probation_does_not_allow_d_matrix():
    r = evaluate_wakeup_probation(market_signals={"hard_gate_pass_rate": 0.05, "market_breadth_pass_rate": 0.05}, previous_state="HIBERNATE")
    assert r["d_matrix_allowed"] is False
    assert r["max_role_allowed"] == "B_MID_ROTATION"
    print("✅ wakeup probation disallows D-Matrix")

if __name__ == "__main__":
    test_wakeup_probation_does_not_allow_d_matrix()
    print("\n🏁 Wakeup Probation tests PASS")
