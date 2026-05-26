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

def test_controller_wakeup_probation_can_be_final_state():
    r = build_tail_risk_controller_preview(
        previous_state="HIBERNATE",
        market_signals={"hard_gate_pass_rate": 0.03, "market_breadth_pass_rate": 0.03},
    )
    assert r["final_state"] == "WAKEUP_PROBATION"
    assert r["final_decision"] == "DOWNGRADE"
    assert r["action_policy_preview"]["allow_d_matrix"] is False
    print("✅ WAKEUP_PROBATION can be final_state")

def test_controller_generates_isolation_even_when_hibernate_overrides_final_decision():
    r = build_tail_risk_controller_preview(
        previous_state="NORMAL",
        market_signals={
            "limit_down_count": 120,
            "hard_gate_pass_rate": 0.005,
            "market_breadth_pass_rate": 0.005,
        },
        position_context={"ticker": "002472", "role": "D_BLACK_HORSE"},
    )
    assert r["final_state"] == "HIBERNATE"
    assert r["final_decision"] == "HIBERNATE"
    assert r["has_isolation_trigger"] is True
    assert r["risk_isolation_preview"]
    assert r["risk_isolation_preview"]["ticker"] == "002472"
    assert r["risk_isolation_preview"]["auto_sell_allowed"] is False
    assert r["risk_isolation_preview"]["broker_order_allowed"] is False
    print("✅ isolation preserved even when HIBERNATE overrides")

def test_controller_action_policy_marks_isolation_review():
    r = build_tail_risk_controller_preview(
        market_signals={"limit_down_count": 120},
        position_context={"ticker": "002472"},
    )
    assert r["action_policy_preview"]["requires_risk_isolation_review"] is True
    print("✅ action policy marks isolation review")

def test_all_gate_results_have_affected_tickers():
    r = build_tail_risk_controller_preview(market_signals={})
    for g in r["gate_results"]:
        assert "affected_tickers" in g, f"gate {g.get('gate_type')} missing affected_tickers"
    print("✅ all gate results have affected_tickers")

if __name__ == "__main__":
    test_controller_hibernates_when_pass_rate_below_1_percent()
    test_controller_no_real_trade_fields_false()
    test_controller_wakeup_probation_can_be_final_state()
    test_controller_generates_isolation_even_when_hibernate_overrides_final_decision()
    test_controller_action_policy_marks_isolation_review()
    test_all_gate_results_have_affected_tickers()
    print("\n🏁 Tail-Risk Controller tests PASS")
