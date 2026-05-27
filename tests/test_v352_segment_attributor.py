from zmatrix.strategy_repair.segment_attributor import build_segment_attribution

def test_segment_attribution_role():
    joined = [{"role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t20": -1, "invalidation_triggered": False, "max_adverse_excursion_pct": -2}, {"role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t20": 3, "invalidation_triggered": False, "max_adverse_excursion_pct": -1}]
    r = build_segment_attribution(joined=joined, horizon="t20")
    assert "B_MID_ROTATION" in r["segments"]["role"]
    assert r["real_trade_allowed"] is False
