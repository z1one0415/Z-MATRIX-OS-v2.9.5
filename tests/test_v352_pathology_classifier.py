from zmatrix.strategy_repair.pathology_classifier import classify_sample_pathology

def test_pathology_negative_b_rotation():
    r = classify_sample_pathology(sample={"paper_id": "p1", "ticker": "000001", "role": "B_MID_ROTATION", "paper_action": "PAPER_WATCH_ROTATION", "outcome_status": "READY", "actual_return_t20": -3.2, "max_adverse_excursion_pct": -12, "invalidation_triggered": True}, horizon="t20")
    assert "NEGATIVE_RETURN" in r["tags"]
    assert "B_ROTATION_LOSER" in r["tags"]
    assert "INVALIDATED" in r["tags"]
    assert r["real_trade_allowed"] is False
