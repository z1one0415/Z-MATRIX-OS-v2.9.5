"""Portfolio Exposure Policy tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.portfolio_exposure.policy import assert_no_real_trade_effects, validate_exposure_record

def test_policy_rejects_auto_sell():
    v = assert_no_real_trade_effects({"safety":{"auto_sell_allowed":True}})
    assert any("auto_sell_allowed" in x for x in v)
    print("✅ rejects auto_sell")

def test_valid_record_passes():
    v = validate_exposure_record({"ticker":"002472"})
    assert v == []
    print("✅ valid passes")

if __name__ == "__main__":
    test_policy_rejects_auto_sell()
    test_valid_record_passes()
    print("\n🏁 Portfolio Policy PASS")
