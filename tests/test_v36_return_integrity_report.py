from zmatrix.return_integrity.return_integrity_report import build_return_integrity_report

def test_return_integrity_report_blocks_live_trade():
    outcomes = [
        {"paper_id": "p1", "outcome_status": "READY", "actual_return_t20": -1},
        {"paper_id": "p2", "outcome_status": "READY", "actual_return_t20": 20},
    ]
    actions = [
        {"paper_id": "p1", "ticker": "000001", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION"},
        {"paper_id": "p2", "ticker": "000002", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION"},
    ]
    r = build_return_integrity_report(outcomes=outcomes, paper_actions=actions, horizon="t20")
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["policy_violations"] == []
