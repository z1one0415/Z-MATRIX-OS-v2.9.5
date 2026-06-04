from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def _s(o):
    for k in["trade_allowed","verdict_allowed","portfolio_decision_allowed","order_generation_allowed","position_sizing_allowed","target_price_allowed","broker_order_allowed","researchdb_main_write"]:
        assert o.get(k) is False,k
def test_has(): assert has_domain_router("PORTFOLIO.GET_SCHEMA")
def test_schema(): r=route_skill_by_domain("PORTFOLIO.GET_SCHEMA",{},{}); assert r["status"]=="EXECUTED"; _s(r["output"])
def test_draft(): r=route_skill_by_domain("PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED"; _s(r["output"])
def test_readiness(): r=route_skill_by_domain("PORTFOLIO.GET_PORTFOLIO_READINESS",{},{}); assert r["output"]["portfolio_engine_enabled"] is False and r["output"]["order_generation_allowed"] is False and r["output"]["position_sizing_allowed"] is False
def test_validate(): r=route_skill_by_domain("PORTFOLIO.VALIDATE_PORTFOLIO_INPUT_DRY",{},{"portfolio_input":{}}); assert r["output"]["dry_run"] is True
