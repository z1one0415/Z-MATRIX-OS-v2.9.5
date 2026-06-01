from zmatrix.agent.skill_invocation import invoke_skill
def _e(sid,risk="R0_READ"): return {"command_id":"t-"+sid,"agent_id":"z-orchestrator","requested_skill":sid,"risk_level":risk,"production_allowed":False,"requires_human_review":risk=="R2_DRAFT","action_intent":"QUERY"}
def test_readiness(): r=invoke_skill(_e("GOVERNANCE.GET_GOVERNANCE_READINESS"),{"token_estimate":100}); assert r["status"]=="EXECUTED"
def test_verify_dry(): r=invoke_skill(_e("GOVERNANCE.RUN_SKILLOS_VERIFY_DRY","R1_ANNOTATE"),{"token_estimate":100}); assert r["output"]["subprocess"] is False
def test_audit_draft(): r=invoke_skill(_e("GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT","R2_DRAFT"),{"token_estimate":100}); assert r["status"]=="DRAFT_CREATED" and r["researchdb_main_write"] is False
