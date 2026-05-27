from zmatrix.invalidation_anatomy.trigger_day_feature_builder import build_trigger_day_features

def test_trigger_day_ohlc_features():
    event = {"event_status": "READY", "paper_id": "p1", "ticker": "000001", "trigger_idx": 0, "trigger_return_pct": -9}
    bars = [{"trade_date": "20240101", "open": 100, "high": 102, "low": 90, "close": 91, "volume": 1000}]
    r = build_trigger_day_features(event=event, price_bars=bars)
    assert r["feature_status"] == "READY"
    assert r["features"]["ohlc_ready"] is True
    assert r["real_trade_allowed"] is False
