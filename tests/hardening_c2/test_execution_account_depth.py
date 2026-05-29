def test_limit_down_sell_failure():
    from zmatrix.execution_quality.execution_depth import LimitDownSellFailureGate
    r = LimitDownSellFailureGate.check({"open":9,"high":9,"low":9,"close":9,"pct_chg":-10})
    assert r.executable == False and r.real_trade_allowed == False and r.action == "NOT_FILLABLE"

def test_suspension_blocks():
    from zmatrix.execution_quality.execution_depth import SuspensionGate
    r = SuspensionGate.check({"suspended": True})
    assert r.real_trade_allowed == False and r.action == "DATA_INSUFFICIENT"

def test_one_price_board():
    from zmatrix.execution_quality.execution_depth import OnePriceBoardDetector
    r = OnePriceBoardDetector.check({"open":10,"high":10,"low":10,"close":10})
    assert r.action == "NOT_FILLABLE"

def test_route_competition():
    from zmatrix.execution_quality.execution_depth import RouteCompetition
    r = RouteCompetition.compare([{"route_id":"twap","cost_bps":5,"fill_probability":0.8},{"route_id":"open","cost_bps":10,"fill_probability":0.2}])
    assert r["winner"] == "twap" and r["real_trade_allowed"] == False

def test_holding_alpha():
    from zmatrix.account_governance.governance_depth import HoldingAlpha
    r = HoldingAlpha.compute("000001",0.12,0.08)
    assert abs(r.alpha-0.04)<1e-9 and r.real_trade_allowed == False

def test_watchlist_curve():
    from zmatrix.account_governance.governance_depth import WatchlistOpportunityCurve
    w = WatchlistOpportunityCurve(); w.append("000001",0.10,0.06)
    s = w.summary()
    assert s["count"]==1 and s["real_trade_allowed"]==False

def test_risk_budget_blocks():
    from zmatrix.account_governance.governance_depth import RiskBudget
    r = RiskBudget.check(-0.12,0.10)
    assert r["action"]=="ACTION_BLOCKED" and r["real_trade_allowed"]==False
