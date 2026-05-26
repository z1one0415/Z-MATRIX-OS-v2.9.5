import sys,os; sys.path.insert(0,'.')
from zmatrix.brd_strategy_validation.validation_policy import validate_v35_report_safety, validate_v35_validation_status

def test_policy():
    assert any("real_trade_allowed" in e for e in validate_v35_report_safety({"real_trade_allowed":True}))
    assert any("safety.runtime_enabled" in e for e in validate_v35_report_safety({"safety":{"runtime_enabled":True}}))
    assert validate_v35_validation_status({"validation_status":"STRATEGY_VALIDATION_REPORT_READY","brd_connected":False,"fallback_rate":0,"metrics":{"valid_outcome_count":10}})
    assert validate_v35_validation_status({"validation_status":"STRATEGY_VALIDATION_REPORT_READY","brd_connected":True,"fallback_rate":0,"metrics":{"valid_outcome_count":0}})
    print("✅ validation policy")

if __name__=="__main__": test_policy(); print("\n🏁 Policy PASS")
