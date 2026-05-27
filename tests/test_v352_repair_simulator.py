from zmatrix.strategy_repair.repair_simulator import run_repair_simulation

def test_repair_simulator_runs():
    joined = [{"paper_id": "p1", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t5": 1, "actual_return_t20": -2, "actual_return_t60": -3, "invalidation_triggered": True, "max_adverse_excursion_pct": -12}, {"paper_id": "p2", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t5": 2, "actual_return_t20": 8, "actual_return_t60": 10, "invalidation_triggered": False, "max_adverse_excursion_pct": -2}]
    r = run_repair_simulation(joined=joined, horizon="t20")
    assert "baseline" in r
    assert "exclude_invalidated" in r["candidates"]
    assert r["real_trade_allowed"] is False
