"""Paper Outcome Policy tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.policy import assert_no_real_trade_effects, validate_outcome_record

def test_policy_rejects_real_trade():
    v = assert_no_real_trade_effects({"safety":{"real_trade_allowed":True}})
    assert any("real_trade_allowed" in x for x in v)
    print("✅ rejects real_trade")

def test_policy_rejects_non_dict_safety():
    v = assert_no_real_trade_effects({"safety":"bad"})
    assert "safety must be dict" in v
    print("✅ rejects non-dict safety")

def test_valid_record_passes():
    v = validate_outcome_record({"paper_id":"p1","ticker":"002472","outcome_status":"READY"})
    assert v == []
    print("✅ valid record passes")

if __name__ == "__main__":
    test_policy_rejects_real_trade()
    test_policy_rejects_non_dict_safety()
    test_valid_record_passes()
    print("\n🏁 Policy PASS")
