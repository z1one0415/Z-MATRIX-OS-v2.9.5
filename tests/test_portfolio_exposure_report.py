"""Portfolio Exposure Report tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.portfolio_exposure.exposure_report import build_exposure_report

def test_exposure_report():
    positions = [{"ticker":"002472","weight":0.30,"sector":"robotics","chain":"机器人"},
                 {"ticker":"601899","weight":0.25,"sector":"mining","chain":"贵金属"}]
    r = build_exposure_report(positions)
    assert r["position_count"] == 2
    assert len(r["sector_exposure"]) == 2
    assert r["real_trade_allowed"] is False
    print("✅ exposure report works")

if __name__ == "__main__":
    test_exposure_report()
    print("\n🏁 Exposure Report PASS")
