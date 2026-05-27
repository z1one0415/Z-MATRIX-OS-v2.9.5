from zmatrix.invalidation_anatomy.pre_trigger_feature_builder import build_pre_trigger_features

def test_pre_trigger_features():
    event = {"event_status": "READY", "paper_id": "p1", "ticker": "000001", "trigger_idx": 2, "entry_price": 100}
    bars = [{"trade_date": "20240101", "close": 100, "volume": 1000}, {"trade_date": "20240102", "close": 95, "volume": 1200}, {"trade_date": "20240103", "close": 91, "volume": 1500}]
    r = build_pre_trigger_features(event=event, price_bars=bars)
    assert r["feature_status"] == "READY"
    assert "drawdown_speed" in r["features"]
    assert r["real_trade_allowed"] is False
