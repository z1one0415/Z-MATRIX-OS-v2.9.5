from zmatrix.agent.skill_invocation import invoke_skill
def _e(sid,risk="R0_READ"): return {"command_id":"t-"+sid,"agent_id":"z-orchestrator","requested_skill":sid,"risk_level":risk,"production_allowed":False,"requires_human_review":risk!="R0_READ","action_intent":"QUERY"}
def test_invoke_rdb(): r=invoke_skill(_e("RESEARCHDB.GET_RESEARCHDB_READINESS"),{"token_estimate":100}); assert r["status"]=="EXECUTED"
def test_invoke_df_schema(): r=invoke_skill(_e("DATAFORGE.GET_SNAPSHOT_SCHEMA"),{"token_estimate":100}); assert r["status"]=="EXECUTED"
def test_invoke_df_dry(): r=invoke_skill(_e("DATAFORGE.VALIDATE_SNAPSHOT_DRY","R1_ANNOTATE"),{"token_estimate":100,"snapshot":{}}); assert r["status"]=="EXECUTED" and r["researchdb_main_write"] is False
