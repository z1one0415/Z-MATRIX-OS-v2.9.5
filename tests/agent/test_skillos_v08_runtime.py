from zmatrix.agent.domain_skill_router import route_skill_by_domain
SK=["external_api_used","production_allowed","shadowbroker_deployed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","final_scoring_allowed","backtest_allowed","researchdb_main_write","memory_main_write"]
def _s(o):
    for k in SK: assert o.get(k) is False,k
def test_zc35(): 
    for sid in["ZC35.GET_SCHEMA","ZC35.GET_CHECKLIST","ZC35.VALIDATE_INPUT_DRY","ZC35.BUILD_REVIEW_DRAFT","ZC35.GET_READINESS"]:
        r=route_skill_by_domain(sid,{},{"zc35_input":{}}); assert r["status"]in{"EXECUTED","DRAFT_CREATED"}; _s(r["output"])
def test_bmatrix():
    for sid in["BMATRIX.GET_SCHEMA","BMATRIX.GET_SCORECARD_TEMPLATE","BMATRIX.VALIDATE_SCORE_INPUT_DRY","BMATRIX.BUILD_REVIEW_DRAFT","BMATRIX.GET_READINESS"]:
        r=route_skill_by_domain(sid,{},{"score_input":{}}); assert r["status"]in{"EXECUTED","DRAFT_CREATED"}; _s(r["output"])
def test_dmatrix():
    for sid in["DMATRIX.GET_SCHEMA","DMATRIX.GET_LIFECYCLE_STAGE_TEMPLATE","DMATRIX.VALIDATE_STAGE_INPUT_DRY","DMATRIX.BUILD_REVIEW_DRAFT","DMATRIX.GET_READINESS"]:
        r=route_skill_by_domain(sid,{},{"stage_input":{}}); assert r["status"]in{"EXECUTED","DRAFT_CREATED"}; _s(r["output"])
