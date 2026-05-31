from zmatrix.agent.skill_domain_registry import has_domain_router, is_domain_registered
from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_core_has_routers():
    for sid in ["SYSTEM.GET_SKILLOS_STATUS","ZG16.GET_SOURCE_REGISTRY","CASEFORGE.GET_CASE_DRAFT_SCHEMA","REPORT.RENDER_SKILLOS_STATUS_DRAFT","COCKPIT.BUILD_SKILLOS_OVERVIEW"]:
        assert is_domain_registered(sid) and has_domain_router(sid)
def test_unimpl_blocks(): assert route_skill_by_domain("FACTOR.CALC",{},{})["status"]=="BLOCKED"
def test_sys_executes(): r=route_skill_by_domain("SYSTEM.GET_SKILLOS_STATUS",{},{}); assert r["status"]=="EXECUTED"
def test_report_draft(): r=route_skill_by_domain("REPORT.RENDER_SKILLOS_STATUS_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["proposal_required"]
def test_cf_no_write(): r=route_skill_by_domain("CASEFORGE.BUILD_INTAKE_DRAFT",{},{}); assert r["output"]["main_write"] is False
