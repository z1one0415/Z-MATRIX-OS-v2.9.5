from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def _s(o):
    for k in["trade_allowed","verdict_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","researchdb_main_write","memory_main_write","final_decision"]:
        assert o[k] is False,k
def test_has(): assert has_domain_router("COUNCIL.GET_COUNCIL_SCHEMA")
def test_schema(): r=route_skill_by_domain("COUNCIL.GET_COUNCIL_SCHEMA",{},{}); assert r["status"]=="EXECUTED"; _s(r["output"])
def test_draft(): r=route_skill_by_domain("COUNCIL.BUILD_EXPERT_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED"; _s(r["output"])
def test_validator(): r=route_skill_by_domain("COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY",{},{"council_output":"BUY 卖出"}); assert r["output"]["valid"] is False
def test_readiness(): r=route_skill_by_domain("COUNCIL.GET_COUNCIL_READINESS",{},{}); assert r["output"]["final_verdict_enabled"] is False
