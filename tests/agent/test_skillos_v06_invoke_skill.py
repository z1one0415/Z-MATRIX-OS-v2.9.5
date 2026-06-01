from zmatrix.agent.skill_invocation import invoke_skill
def _e(sid,risk="R0_READ"): return {"command_id":"t-"+sid,"agent_id":"z-orchestrator","requested_skill":sid,"risk_level":risk,"production_allowed":False,"requires_human_review":risk=="R2_DRAFT","action_intent":"QUERY"}
def test_registry(): r=invoke_skill(_e("FACTOR.GET_FACTOR_REGISTRY"),{"token_estimate":100}); assert r["status"]=="EXECUTED"
def test_readiness(): r=invoke_skill(_e("FACTOR.GET_FACTOR_READINESS"),{"token_estimate":100}); o=r["output"]; assert o["factor_engine_enabled"] is False and o["ranking_allowed"] is False
def test_draft(): r=invoke_skill(_e("FACTOR.BUILD_FACTOR_REVIEW_DRAFT","R2_DRAFT"),{"token_estimate":100}); assert r["status"]=="DRAFT_CREATED"
