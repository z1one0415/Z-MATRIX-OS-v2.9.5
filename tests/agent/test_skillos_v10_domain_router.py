from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def _s(o):
    for k in["trade_allowed","verdict_allowed","workflow_execution_allowed","multi_domain_execution_allowed","portfolio_decision_allowed","order_generation_allowed","researchdb_main_write"]:
        assert o.get(k) is False,k
def test_has(): assert has_domain_router("WORKFLOW.GET_WORKFLOW_SCHEMA")
def test_schema(): r=route_skill_by_domain("WORKFLOW.GET_WORKFLOW_SCHEMA",{},{}); assert r["status"]=="EXECUTED";_s(r["output"])
def test_draft(): r=route_skill_by_domain("WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED";_s(r["output"])
def test_dry(): r=route_skill_by_domain("WORKFLOW.RUN_RESEARCH_DRY_CHAIN",{},{}); assert r["output"]["dry_run"] and r["output"]["workflow_execution_allowed"] is False
def test_readiness(): r=route_skill_by_domain("WORKFLOW.GET_WORKFLOW_READINESS",{},{}); o=r["output"]; assert o["workflow_engine_enabled"] is False and o["workflow_execution_allowed"] is False and o["multi_domain_execution_allowed"] is False
