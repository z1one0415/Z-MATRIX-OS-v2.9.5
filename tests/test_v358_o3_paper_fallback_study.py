from zmatrix.regime_observation.o3_paper_fallback_study import build_o3_paper_fallback_study

def test_fallback_required():
    r = build_o3_paper_fallback_study(pool_deep_dive={"policy_pool_deep_results":{"test":{"pool_resilience_deep_status":"POOL_RESILIENCE_WARNING","reasons":["CONCENTRATED_POLICY_RISK"]}}})
    assert r["fallback_study_status"] == "FALLBACK_OBSERVATION_POOL_REQUIRED"
    assert r["o3_conditional_runtime_enabled"] is False
