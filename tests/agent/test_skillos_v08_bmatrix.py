from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def _s(o):
    for k in["trade_allowed","verdict_allowed","final_scoring_allowed","backtest_allowed","researchdb_main_write"]:
        assert o[k] is False,k
def test_has(): assert has_domain_router("BMATRIX.GET_SCHEMA")
def test_schema(): r=route_skill_by_domain("BMATRIX.GET_SCHEMA",{},{}); assert r["status"]=="EXECUTED";_s(r["output"])
def test_draft(): r=route_skill_by_domain("BMATRIX.BUILD_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED";_s(r["output"])
