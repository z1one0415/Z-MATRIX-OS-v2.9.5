from zmatrix.regime_attribution.regime_performance_profiler import profile_regime_performance

def test_regime_performance_profile():
    rows = [{"market_regime":"BULL_TREND","actual_return_t20":5,"invalidation_triggered":False}]*100 + [{"market_regime":"BEAR_TREND","actual_return_t20":-3,"invalidation_triggered":True}]*50
    r = profile_regime_performance(enriched_rows=rows)
    assert "BULL_TREND" in r["market_regime_profiles"]
    assert "BEAR_TREND" in r["market_regime_profiles"]
    assert r["real_trade_allowed"] is False
