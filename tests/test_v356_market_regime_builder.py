from zmatrix.regime_attribution.market_regime_builder import build_market_regime, classify_market_regime

def test_regime_missing_index_data():
    r = classify_market_regime(index_features=None)
    assert r["regime"] == "UNKNOWN_MARKET_REGIME"
    assert r["real_trade_allowed"] is False
    assert r["uses_future_data"] is False
