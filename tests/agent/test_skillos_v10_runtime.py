from zmatrix.agent.domain_skill_router import route_skill_by_domain
SK=["external_api_used","production_allowed","shadowbroker_deployed","trade_allowed","verdict_allowed","broker_runtime_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_decision_allowed","position_sizing_allowed","order_generation_allowed","target_price_allowed","workflow_execution_allowed","multi_domain_execution_allowed","researchdb_main_write","memory_main_write"]
def _s(o):
    for k in SK: assert o.get(k) is False,k
def test_all():
    for sid in["WORKFLOW.GET_WORKFLOW_SCHEMA","WORKFLOW.GET_STAGE_TEMPLATE","WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT","WORKFLOW.BUILD_MULTI_DOMAIN_REVIEW_DRAFT","WORKFLOW.RUN_RESEARCH_DRY_CHAIN","WORKFLOW.VALIDATE_WORKFLOW_INPUT_DRY","WORKFLOW.GET_WORKFLOW_READINESS"]:
        r=route_skill_by_domain(sid,{},{"workflow_input":{}}); assert r["status"]in{"EXECUTED","DRAFT_CREATED"}; _s(r["output"])
def test_draft():
    for sid in["WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT","WORKFLOW.BUILD_MULTI_DOMAIN_REVIEW_DRAFT"]:
        r=route_skill_by_domain(sid,{},{}); assert r["status"]=="DRAFT_CREATED" and r["human_review_required"]
def test_dry():
    o=route_skill_by_domain("WORKFLOW.RUN_RESEARCH_DRY_CHAIN",{},{}); o=o["output"]; assert o["dry_run"] and o["plan_only"] and o["workflow_execution_allowed"] is False
def test_readiness():
    o=route_skill_by_domain("WORKFLOW.GET_WORKFLOW_READINESS",{},{}); o=o["output"]
    for k in["workflow_engine_enabled","workflow_execution_allowed","multi_domain_execution_allowed","external_api_used","production_allowed","broker_runtime_allowed","broker_order_allowed","real_trade_allowed","order_generation_allowed","portfolio_decision_allowed","trade_signal_allowed","buy_sell_hold_allowed","position_sizing_allowed","target_price_allowed","researchdb_main_write","memory_main_write"]:
        assert o[k] is False,k
