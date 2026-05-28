from zmatrix.regime_conditioned_replay.replay_report_builder import build_replay_report

def test_replay_report_no_runtime():
    joined = [{"paper_id":"p1","ticker":"000001","entry_date":"20240101","actual_return_t20":-2,"invalidation_triggered":True,"role":"B_MID_ROTATION"}]
    r = build_replay_report(joined=joined, data_root=".", max_items=1)
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["policy_violations"] == []
