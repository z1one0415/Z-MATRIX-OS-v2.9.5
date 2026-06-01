from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_has(): assert has_domain_router("GOVERNANCE.GET_VERIFY_SCRIPT_REGISTRY")
def test_no_subprocess(): r=route_skill_by_domain("GOVERNANCE.RUN_SKILLOS_VERIFY_DRY",{},{}); assert r["status"]=="EXECUTED" and r["output"]["subprocess"] is False
def test_ledger(): r=route_skill_by_domain("GOVERNANCE.GET_LEDGER_STATUS",{},{}); assert r["status"]=="EXECUTED" and "all_empty" in r["output"]
def test_registry_dry(): r=route_skill_by_domain("GOVERNANCE.VALIDATE_SKILL_REGISTRY_DRY",{},{}); assert r["output"]["dry"] and r["output"]["main_write"] is False
def test_audit_draft(): r=route_skill_by_domain("GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["human_review_required"]
