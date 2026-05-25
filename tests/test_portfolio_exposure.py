"""Portfolio Exposure v1.0 tests"""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.portfolio_exposure import analyze_portfolio_exposure

def test_required_fields():
    r = analyze_portfolio_exposure({"ticker":"002472","chain":"ROBOT","sector":"MACHINERY"})
    for k in ["market_beta","sector_beta","max_drawdown","correlation_60d","correlation_120d","correlation_250d","degraded","exposure_gate_passed","add_position_allowed","warnings"]:
        assert k in r, f"missing {k}"
    print("✅ portfolio_exposure: required fields present")

def test_degraded_on_missing_history():
    r = analyze_portfolio_exposure({"ticker":"002472"})
    assert r["degraded"] is True
    assert r["exposure_gate_passed"] is False
    assert r["add_position_allowed"] is False
    assert "INSUFFICIENT_5Y_EXPOSURE_DATA" in str(r["warnings"])
    print("✅ portfolio_exposure: DEGRADED on missing history")

def test_allowed_with_full_data():
    candidate = {"ticker":"002472","chain":"ROBOT","sector":"MACHINERY","market_beta":1.2,"sector_beta":0.9,"max_drawdown":-25,"correlation_60d":0.6,"correlation_120d":0.5,"correlation_250d":0.4}
    r = analyze_portfolio_exposure(candidate)
    assert r["degraded"] is False
    print(f"✅ portfolio_exposure: not degraded, {len(r['warnings'])} warnings")

def test_no_forbidden():
    r = analyze_portfolio_exposure({"ticker":"002472"})
    for t in ["BUY","SELL","AUTO_TRADE","MARKET_ORDER","BROKER_ORDER","REAL_TRADE"]:
        assert t not in json.dumps(r)
    print("✅ portfolio_exposure: no forbidden tokens")

if __name__ == "__main__":
    test_required_fields(); test_degraded_on_missing_history(); test_allowed_with_full_data(); test_no_forbidden()
    print("\n🏁 Portfolio Exposure — tests PASS")
