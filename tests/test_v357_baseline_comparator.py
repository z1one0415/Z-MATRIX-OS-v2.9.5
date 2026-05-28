from zmatrix.regime_conditioned_replay.baseline_comparator import compare_all_policies

def test_baseline_comparison():
    replay = {"baseline_raw":{"win_rate":0.45,"median":-1.0,"mean":1.5},"policy_results":{"test_policy":{"metrics":{"win_rate":0.50,"median":-0.5,"mean":2.0},"kept_count":5000,"kept_rate":0.5,"downgraded_count":5000,"opportunity_loss_rate":0.3}}}
    r = compare_all_policies(replay=replay)
    assert r["policy_comparisons"]["test_policy"]["win_rate_delta"] == 0.05
    assert r["real_trade_allowed"] is False
