from zmatrix.invalidation_anatomy.recovery_profile_classifier import build_recovery_profile

def test_recovery_profile():
    event = {"event_status": "READY", "paper_id": "p1", "ticker": "000001", "trigger_idx": 0, "entry_price": 100}
    bars = [{"trade_date": "20240101", "close": 91}, {"trade_date": "20240102", "close": 96}, {"trade_date": "20240103", "close": 101}]
    r = build_recovery_profile(event=event, price_bars=bars)
    assert r["profile_status"] == "READY"
    assert "rebound_after_trigger_1d" in r
