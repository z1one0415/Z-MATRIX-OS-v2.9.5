from zmatrix.regime_observation.pool_resilience_deep_dive import deep_dive_pool_resilience

def test_pool_concentrated():
    replay = {"policy_results":{"test":{"kept_count":100,"kept_rate":0.25,"kept_rows":[{"ticker":"000001"}]*30+[{"ticker":"000002"}]*70,"downgraded_rows":[]}}}
    gov = {"candidate_pool_resilience":{"policy_pool_results":{"test":{"kept_rate":0.25,"daily_pool_stats":{}}}}}
    r = deep_dive_pool_resilience(replay_report=replay, governance_report=gov)
    assert r["policy_pool_deep_results"]["test"]["pool_resilience_deep_status"] == "POOL_RESILIENCE_WARNING"
