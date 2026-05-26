"""Paper Outcome Policy tests — full blocked fields"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.policy import assert_no_real_trade_effects, validate_outcome_record

def test_policy_rejects_real_trade():
    v = assert_no_real_trade_effects({"safety":{"real_trade_allowed":True}})
    assert any("real_trade_allowed" in x for x in v)
    print("✅ rejects real_trade")

def test_policy_rejects_system_prompt_write():
    v = assert_no_real_trade_effects({"safety":{"system_prompt_write_allowed":True}})
    assert any("system_prompt_write" in x for x in v)
    print("✅ rejects system_prompt_write")

def test_policy_rejects_runtime_injection():
    v = assert_no_real_trade_effects({"safety":{"runtime_injection_allowed":True}})
    assert any("runtime_injection" in x for x in v)
    print("✅ rejects runtime_injection")

def test_valid_record_passes():
    v = validate_outcome_record({"paper_id":"p1","ticker":"002472","outcome_status":"READY"})
    assert v == []
    print("✅ valid record passes")

if __name__ == "__main__":
    test_policy_rejects_real_trade()
    test_policy_rejects_system_prompt_write()
    test_policy_rejects_runtime_injection()
    test_valid_record_passes()
    print("\n🏁 Policy PASS")
