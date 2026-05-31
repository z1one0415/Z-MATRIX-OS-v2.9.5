from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_has(): assert has_domain_router("AUTOCASE.GET_INTAKE_SCHEMA") and has_domain_router("MEMORY.GET_MEMORY_CANDIDATE_SCHEMA")
def test_ac_draft(): r=route_skill_by_domain("AUTOCASE.BUILD_CASE_CANDIDATE_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["output"]["main_write"] is False
def test_mm_draft(): r=route_skill_by_domain("MEMORY.BUILD_MONTHLY_MEMORY_CANDIDATE_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["output"]["main_write"] is False
