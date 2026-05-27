from zmatrix.paper_repair_replay.repair_replay_report import build_paper_repair_replay_report

def test_repair_replay_report_policy():
    joined = [{"paper_id": "p1", "ticker": "000001", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "entry_date": "20240101", "entry_price": 100, "max_loss_plan": 8, "baseline_return_t20": -20}]
    r = build_paper_repair_replay_report(joined=joined, data_root="/tmp/nonexistent", horizon_days=20)
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
