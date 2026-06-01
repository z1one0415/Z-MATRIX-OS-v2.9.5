from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_has(): assert has_domain_router("GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY")
def test_verify_dry_no_shell(): r=route_skill_by_domain("GOVERNANCE.RUN_SKILLOS_VERIFY_DRY",{},{}); assert r["output"]["subprocess_execution"] is False
def test_forbidden_scan(): r=route_skill_by_domain("GOVERNANCE.GET_FORBIDDEN_SCAN_STATUS",{},{}); assert "hit_count" in r["output"] and "ok" in r["output"]
def test_audit_draft(): r=route_skill_by_domain("GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["researchdb_main_write"] is False
def test_registry_dry(): r=route_skill_by_domain("GOVERNANCE.VALIDATE_SKILL_REGISTRY_DRY",{},{}); assert r["output"]["subprocess_execution"] is False and r["output"]["main_write"] is False
