from zmatrix.regime_conditioned_replay.candidate_verdict import judge_replay_candidate

def test_full_sample_pass_not_production_ready():
    r = judge_replay_candidate(result={"metrics":{"win_rate":0.6,"median":2.0,"top_1pct_contribution":0.3,"trimmed_mean_5pct":1.0},"delta_vs_raw":{"win_rate_delta":0.10,"median_delta":1.5,"trimmed_mean_delta":0.5},"kept_count":5000,"kept_rate":0.25,"downgraded_count":15000,"opportunity_loss_rate":0.3,"policy":{"lookahead_risk":False,"production_ready":False}})
    assert r["status"] == "POLICY_FULL_SAMPLE_PASS_STABILITY_PENDING"
    assert r["requires_anti_overfit_validation"] is True
    assert r["production_ready"] is False
