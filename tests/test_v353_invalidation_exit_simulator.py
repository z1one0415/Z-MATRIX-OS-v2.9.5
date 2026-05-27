from zmatrix.paper_repair_replay.invalidation_exit_simulator import simulate_invalidation_exit

def test_invalidation_exit_triggered():
    action = {"paper_id": "p1", "ticker": "000001", "entry_price": 100, "entry_date": "20240101", "role": "B_MID_ROTATION"}
    path = {"bars": [{"trade_date": "20240101", "close": 100}, {"trade_date": "20240102", "close": 97}, {"trade_date": "20240103", "close": 91}]}
    rule = {"max_loss_pct": -8}
    r = simulate_invalidation_exit(action=action, price_path=path, rule=rule, horizon_days=20)
    assert r["exit_triggered"] is True
    assert r["exit_reason"] == "INVALIDATION_EXIT_TRIGGERED"
    assert r["repaired_return"] == -9
    assert r["real_trade_allowed"] is False
