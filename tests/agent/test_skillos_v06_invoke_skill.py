from zmatrix.agent.skill_invocation import invoke_skill
def _e(sid,risk="R0_READ"): return {"command_id":"t-"+sid,"agent_id":"z-orchestrator","requested_skill":sid,"risk_level":risk,"production_allowed":False,"requires_human_review":risk=="R2_DRAFT","action_intent":"QUERY"}
def test_registry(): r=invoke_skill(_e("FACTOR.GET_FACTOR_REGISTRY"),{"token_estimate":100}); assert r["status"]=="EXECUTED" and r["output"]["factor_calculation_allowed"] is False
def test_dry(): r=invoke_skill(_e("FACTOR.VALIDATE_FACTOR_INPUT_DRY","R1_ANNOTATE"),{"token_estimate":100,"factor_input":{}}); assert r["output"]["calculation_executed"] is False
def test_draft(): r=invoke_skill(_e("FACTOR.BUILD_FACTOR_REVIEW_DRAFT","R2_DRAFT"),{"token_estimate":100}); assert r["status"]=="DRAFT_CREATED"
