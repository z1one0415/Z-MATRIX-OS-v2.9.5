from zmatrix.regime_conditioned_replay.replay_metrics import build_replay_metrics

def test_metrics_not_double_scaled():
    rows = [{"actual_return_t20":1.5,"invalidation_triggered":False},{"actual_return_t20":-0.7,"invalidation_triggered":True}]
    r = build_replay_metrics(rows=rows)
    assert r["mean"] == 0.4
    assert r["median"] == 0.4
    assert r["count"] == 2
