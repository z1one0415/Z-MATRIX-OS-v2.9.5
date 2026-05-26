"""Tail-Risk Policy tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.tail_risk.policy import assert_no_real_trade_effects, validate_tail_risk_result, validate_action_downgrade

def test_tail_risk_policy_rejects_auto_sell_true():
    v = assert_no_real_trade_effects({"safety": {"auto_sell_allowed": True}})
    assert any("auto_sell_allowed" in x for x in v)
    print("✅ policy rejects auto_sell")

def test_tail_risk_policy_rejects_broker_order_true():
    v = assert_no_real_trade_effects({"safety": {"broker_order_allowed": True}})
    assert any("broker_order_allowed" in x for x in v)
    print("✅ policy rejects broker_order")

def test_hibernate_requires_human_review():
    result = {"gate_id": "g1", "decision": "HIBERNATE", "action_downgrade": "FREEZE_TO_HIBERNATE",
              "requires_human_review": False, "safety": {}}
    v = validate_tail_risk_result(result)
    assert any("requires human review" in x for x in v)
    print("✅ HIBERNATE requires human review")

def test_policy_rejects_nested_safety_auto_sell_true():
    r = {"safety": {"auto_sell_allowed": True}}
    errors = assert_no_real_trade_effects(r)
    assert any("safety.auto_sell_allowed" in e for e in errors)
    print("✅ policy rejects nested safety.auto_sell_allowed")

def test_policy_rejects_non_dict_safety():
    r = {"safety": "bad"}
    errors = assert_no_real_trade_effects(r)
    assert "safety must be dict" in errors
    print("✅ policy rejects non-dict safety")

if __name__ == "__main__":
    test_tail_risk_policy_rejects_auto_sell_true()
    test_tail_risk_policy_rejects_broker_order_true()
    test_hibernate_requires_human_review()
    test_policy_rejects_nested_safety_auto_sell_true()
    test_policy_rejects_non_dict_safety()
    print("\n🏁 Tail-Risk Policy tests PASS")
