"""Account Constitution v1.0 tests"""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.account_constitution import check_account_constitution

def test_required_fields():
    r = check_account_constitution({"ticker":"002472","role":"A_LONG_CORE"}, {"current_base_bucket_pct":20,"current_cash_pct":30})
    for k in ["account_gate_passed","violation_reasons","current_base_bucket_pct","real_trade_allowed"]:
        assert k in r, f"missing {k}"
    assert r["real_trade_allowed"] is False
    print("✅ account_constitution: required fields")

def test_base_bucket_overflow():
    r = check_account_constitution({"ticker":"002472","role":"A_LONG_CORE"}, {"current_base_bucket_pct":38,"current_cash_pct":30,"add_weight_pct":5})
    assert r["account_gate_passed"] is False, "should block overflow"
    assert any("BASE_BUCKET" in v for v in r["violation_reasons"])
    print("✅ account_constitution: base bucket overflow blocked")

def test_pass():
    r = check_account_constitution({"ticker":"002472","role":"A_LONG_CORE"}, {"current_base_bucket_pct":20,"current_cash_pct":30})
    assert r["account_gate_passed"] is True
    print("✅ account_constitution: PASS")

def test_no_forbidden():
    r = check_account_constitution({"ticker":"002472","role":"WATCH_ONLY"}, {})
    for t in ["BUY","SELL","AUTO_TRADE","MARKET_ORDER","BROKER_ORDER","REAL_TRADE"]:
        assert t not in json.dumps(r)
    print("✅ account_constitution: no forbidden")

if __name__ == "__main__":
    test_required_fields(); test_base_bucket_overflow(); test_pass(); test_no_forbidden()
    print("\n🏁 Account Constitution — tests PASS")
