from zmatrix.regime_observation.zg18_conflict_observer import observe_zg18_conflicts

def test_bull_only_conflict():
    r = observe_zg18_conflicts(full_sample_pass_policies=["allow_b_rotation_in_bull_trend_only"])
    assert r["conflict_observation_status"] == "CONFLICT_RISK_WARNING"
    assert r["g18_conflict_resolver_write_allowed"] is False
