"""Portfolio Exposure Report tests — full components"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.portfolio_exposure.exposure_report import build_exposure_report

def test_exposure_report():
    positions = [{"ticker":"002472","role":"A_LONG_CORE","weight":0.56,"sector":"robotics","chain":"机器人","entry_price":41.71,"current_price":44.01,"beta":1.2},
                 {"ticker":"601899","role":"B_MID_ROTATION","weight":0.24,"sector":"mining","chain":"贵金属","entry_price":34.48,"current_price":31.16,"beta":1.0}]
    r = build_exposure_report(positions)
    assert r["position_count"] == 2
    assert "single_name_exposure" in r
    assert "concentration_warnings" in r
    assert "max_loss_budget" in r
    assert r["real_trade_allowed"] is False
    print(f"✅ full report: {len(r['single_name_exposure'])} positions, {r['concentration_breach_count']} breaches")

if __name__ == "__main__":
    test_exposure_report()
    print("\n🏁 Exposure Report PASS")
