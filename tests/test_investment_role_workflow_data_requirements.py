"""Investment Role Workflow Data Requirements — v2.9.9-dev"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.investment_role_workflow import build_investment_role_review

FULL = {
    "sector":"机器人","sector_stage":"CONFIRMATION","chain":"机器人",
    "force_scores":{"financial_cycle":7,"state_capital":8},
    "fundamentals":{"financial_health_score":8,"quality_score":7,"cashflow_score":8,"roe_score":15,"industry_durability":8,"dividend_or_core_asset_score":6,"sector":"ROBOT","revenue_growth":15,"net_profit_growth":20,"deducted_net_profit_growth":18,"gross_margin":45,"operating_cashflow":100,"debt_ratio":40,"valuation_percentile":60},
    "valuation":{"valuation_safety":7},
    "narrative":{},"event":{},
    "r_matrix":{"status":"DEGRADED","r_action_cap":"WAIT","ticker":"002472"},
    "market_beta":1.2,"sector_beta":0.9,"max_drawdown":-25,"correlation_60d":0.6,"correlation_120d":0.5,"correlation_250d":0.4,
    "checklist":{"stock_role":"A_LONG_CORE","buy_logic_type":"FUNDAMENTAL","sector_stage":"CONFIRMATION","financial_gate_passed":True,"valuation_overheated":False,"max_loss_after_entry":10,"invalidation_condition":"业绩miss","lower_risk_validation_action":"等Q3"},
}

def test_data_requirements_fields():
    r = build_investment_role_review("002472", FULL)
    assert r.get("paper_ledger_required") is True
    assert r.get("outcome_backfill_required") is True
    assert r.get("data_fact_required") is True
    print("✅ data requirements: paper_ledger/outcome_backfill/data_fact all required")

def test_next_workflow_set():
    r = build_investment_role_review("002472", FULL)
    nw = r.get("next_required_workflow")
    assert nw is not None
    assert "paper_trade" in nw or "ledger" in nw
    print(f"✅ next_required_workflow: {nw}")

def test_next_workflow_none_when_not_allowed():
    r = build_investment_role_review("002472", {})
    nw = r.get("next_required_workflow")
    assert nw is None, f"expected None, got {nw}"
    print("✅ next_required_workflow: None (paper not allowed)")

if __name__ == "__main__":
    test_data_requirements_fields(); test_next_workflow_set(); test_next_workflow_none_when_not_allowed()
    print("\n🏁 Data Requirements — tests PASS")
