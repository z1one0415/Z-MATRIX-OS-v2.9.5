from zmatrix.regime_conditioned_replay.regime_policy_replay import run_regime_policy_replay

def test_regime_policy_replay_runs():
    rows = [{"market_regime":"BULL_TREND","actual_return_t20":5,"invalidation_triggered":False}] * 10 + [{"market_regime":"BEAR_TREND","actual_return_t20":-3,"invalidation_triggered":True}] * 5
    r = run_regime_policy_replay(rows=rows)
    assert "baseline_raw" in r
    assert "block_b_rotation_in_bear_trend" in r["policy_results"]
    assert r["real_trade_allowed"] is False
