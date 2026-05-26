"""Tail-Risk Controller tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.tail_risk_controller import build_tail_risk_controller_preview

def test_controller_hibernates_when_pass_rate_below_1_percent():
    r = build_tail_risk_controller_preview(market_signals={"hard_gate_pass_rate": 0.005})
    assert r["final_state"] == "HIBERNATE"
    assert r["action_policy_preview"]["allow_new_entry"] is False
    print("✅ controller hibernates at <1% pass rate")

def test_controller_no_real_trade_fields_false():
    r = build_tail_risk_controller_preview(market_signals={})
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["auto_sell_allowed"] is False
    assert r["auto_buy_allowed"] is False
    print("✅ controller all real trade fields False")

if __name__ == "__main__":
    test_controller_hibernates_when_pass_rate_below_1_percent()
    test_controller_no_real_trade_fields_false()
    print("\n🏁 Tail-Risk Controller tests PASS")
