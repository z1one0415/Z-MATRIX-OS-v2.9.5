from zmatrix.governance_closeout.o3_conditional_fallback_planner import build_o3_conditional_fallback_plan

def test_fallback_required_when_risky():
    r = build_o3_conditional_fallback_plan(pool_resilience={"policy_pool_results":{"test":{"pool_resilience_status":"POOL_RESILIENCE_WARNING","reasons":["CONCENTRATED_POLICY_RISK"]}}})
    assert r["fallback_plan_status"] == "FALLBACK_PLAN_REQUIRED"
    assert r["o3_conditional_runtime_enabled"] is False
