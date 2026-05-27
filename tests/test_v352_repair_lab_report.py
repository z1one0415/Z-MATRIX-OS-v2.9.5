from zmatrix.strategy_repair.repair_lab_report import build_strategy_repair_lab_report

def test_repair_lab_report_no_runtime():
    joined = [{"paper_id": "p1", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t5": 1, "actual_return_t20": -2, "actual_return_t60": -3, "invalidation_triggered": True, "max_adverse_excursion_pct": -12}, {"paper_id": "p2", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t5": 2, "actual_return_t20": 8, "actual_return_t60": 10, "invalidation_triggered": False, "max_adverse_excursion_pct": -2}]
    r = build_strategy_repair_lab_report(joined=joined, horizon="t20")
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["policy_violations"] == []
