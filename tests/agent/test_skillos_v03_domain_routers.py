from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_has_routers(): assert has_domain_router("RESEARCHDB.GET_LAYER_STATUS") and has_domain_router("DATAFORGE.GET_SNAPSHOT_SCHEMA")
def test_rdb_executes(): r=route_skill_by_domain("RESEARCHDB.GET_SKILL_REGISTRY_VIEW",{},{}); assert r["status"]=="EXECUTED" and r["production_allowed"] is False
def test_df_executes(): r=route_skill_by_domain("DATAFORGE.GET_SNAPSHOT_SCHEMA",{},{}); assert r["status"]=="EXECUTED" and r["external_api_used"] is False
def test_df_dry_no_write(): r=route_skill_by_domain("DATAFORGE.VALIDATE_SNAPSHOT_DRY",{},{"snapshot":{}}); assert r["researchdb_main_write"] is False
def test_factor_blocked(): assert route_skill_by_domain("FACTOR.CALC",{},{})["status"]=="BLOCKED"
