from zmatrix.regime_conditioned_replay.candidate_verdict import judge_replay_candidate

def test_verdict_rejects_low_sample():
    r = judge_replay_candidate(result={"metrics":{"win_rate":0.6,"median":2.0,"mean":3.0,"top_1pct_contribution":0.3,"trimmed_mean_5pct":1.0},"delta_vs_raw":{"win_rate_delta":0.10,"median_delta":1.5,"trimmed_mean_delta":0.5},"kept_count":100,"kept_rate":0.05,"downgraded_count":5000,"opportunity_loss_rate":0.3,"policy":{"lookahead_risk":False,"production_ready":False}})
    assert r["status"] == "POLICY_REJECTED_NO_IMPROVEMENT"
    assert "LOW_SAMPLE_COUNT" in r["reasons"]
    assert r["production_ready"] is False
