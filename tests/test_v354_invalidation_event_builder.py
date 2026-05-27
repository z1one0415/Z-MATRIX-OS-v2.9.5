from zmatrix.invalidation_anatomy.invalidation_event_builder import build_invalidation_event

def test_build_invalidation_event():
    sample = {"paper_id": "p1", "ticker": "000001", "entry_price": 100, "entry_date": "20240101"}
    bars = [{"trade_date": "20240101", "close": 100}, {"trade_date": "20240102", "close": 95}, {"trade_date": "20240103", "close": 91}]
    r = build_invalidation_event(sample=sample, price_bars=bars)
    assert r["event_status"] == "READY"
    assert r["trigger_idx"] == 2
    assert r["must_not_use_as_live_decision"] is True
    assert r["real_trade_allowed"] is False
