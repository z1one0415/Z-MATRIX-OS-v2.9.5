from zmatrix.agent.skill_invocation import invoke_skill
def _e(sid,risk="R0_READ"): return {"command_id":"t-"+sid,"agent_id":"z-orchestrator","requested_skill":sid,"risk_level":risk,"production_allowed":False,"requires_human_review":risk=="R2_DRAFT","action_intent":"QUERY"}
def test_schema(): r=invoke_skill(_e("COUNCIL.GET_COUNCIL_SCHEMA"),{"token_estimate":100}); assert r["status"]=="EXECUTED"
def test_draft(): r=invoke_skill(_e("COUNCIL.BUILD_EXPERT_REVIEW_DRAFT","R2_DRAFT"),{"token_estimate":100}); assert r["status"]=="DRAFT_CREATED" and r["output"]["trade_signal_allowed"] is False
def test_validator(): r=invoke_skill(_e("COUNCIL.VALIDATE_COUNCIL_OUTPUT_DRY","R1_ANNOTATE"),{"token_estimate":100,"council_output":"买入"}); assert r["output"]["valid"] is False
