from zmatrix.agent.domain_skill_router import route_skill_by_domain
SK=["external_api_used","production_allowed","shadowbroker_deployed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","portfolio_decision_allowed","position_sizing_allowed","order_generation_allowed","target_price_allowed","researchdb_main_write","memory_main_write"]
def _s(o):
    for k in SK: assert o.get(k) is False,k
def test_all_skills():
    for sid in["PORTFOLIO.GET_SCHEMA","PORTFOLIO.GET_RISK_BUDGET_TEMPLATE","PORTFOLIO.GET_EXPOSURE_TEMPLATE","PORTFOLIO.VALIDATE_PORTFOLIO_INPUT_DRY","PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT","PORTFOLIO.GET_PORTFOLIO_READINESS"]:
        r=route_skill_by_domain(sid,{},{"portfolio_input":{}}); assert r["status"]in{"EXECUTED","DRAFT_CREATED"}; _s(r["output"])
def test_draft_review():
    r=route_skill_by_domain("PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["human_review_required"]
def test_readiness():
    o=route_skill_by_domain("PORTFOLIO.GET_PORTFOLIO_READINESS",{},{}); o=o["output"]
    for k in["portfolio_engine_enabled","portfolio_allowed","portfolio_decision_allowed","order_generation_allowed","position_sizing_allowed","target_price_allowed","trade_signal_allowed","buy_sell_hold_allowed","broker_order_allowed","real_trade_allowed"]:
        assert o[k] is False,k
