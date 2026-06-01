from zmatrix.agent.skill_domain_registry import has_domain_router; from zmatrix.agent.domain_skill_router import route_skill_by_domain
def test_has(): assert has_domain_router("FACTOR.GET_FACTOR_REGISTRY")
def test_registry_no_calc(): r=route_skill_by_domain("FACTOR.GET_FACTOR_REGISTRY",{},{}); assert r["output"]["factor_calculation_allowed"] is False and r["output"]["trading_signal_allowed"] is False
def test_validate_dry(): r=route_skill_by_domain("FACTOR.VALIDATE_FACTOR_INPUT_DRY",{},{"factor_input":{}}); assert r["output"]["calculation_executed"] is False and r["output"]["backtest_executed"] is False
def test_draft(): r=route_skill_by_domain("FACTOR.BUILD_FACTOR_REVIEW_DRAFT",{},{}); assert r["status"]=="DRAFT_CREATED" and r["output"]["trading_signal_allowed"] is False
