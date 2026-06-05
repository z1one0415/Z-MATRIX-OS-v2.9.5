from zmatrix.agent.skill_domain_registry import has_domain_router
from zmatrix.agent.domain_skill_router import route_skill_by_domain
def _tj(*p): return "".join(p)
def _s(o):
    for k in["external_api_used","production_allowed","shadowbroker_deployed","trade_allowed","verdict_allowed","broker_order_allowed","real_trade_allowed","auto_buy_allowed","auto_sell_allowed","investment_verdict_allowed","trade_signal_allowed","buy_sell_hold_allowed","portfolio_allowed","researchdb_main_write","memory_main_write","final_decision"]:
        assert o[k] is False,k
def test_has(): assert has_domain_router("COUNCIL.GET_COUNCIL_SCHEMA")
def test_schema(): r=route_skill_by_domain("COUNCIL.GET_COUNCIL_SCHEMA",{},{}); assert r["status"]=="EXECUTED";_s(r["output"])
def test_draft(): r=route_skill_by_domain("COUNCIL.BUILD_EXPERT_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED";_s(r["output"])
def test_matrix(): r=route_skill_by_domain("COUNCIL.BUILD_DISAGREEMENT_MATRIX_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED";_s(r["output"])
def test_risk(): r=route_skill_by_domain("COUNCIL.BUILD_RISK_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED";_s(r["output"])
def test_validator():
    ft=_tj("B","UY"," ","卖","出")
    r=route_skill_by_domain("COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY",{},{"council_output":ft})
    assert r["output"]["valid"] is False; assert _tj("B","UY") in r["output"]["forbidden_hits"]; assert _tj("卖","出") in r["output"]["forbidden_hits"]; _s(r["output"])
def test_readiness(): r=route_skill_by_domain("COUNCIL.GET_COUNCIL_READINESS",{},{}); assert r["output"]["final_verdict_enabled"] is False and r["output"]["trade_signal_enabled"] is False and r["output"]["portfolio_enabled"] is False; _s(r["output"])
