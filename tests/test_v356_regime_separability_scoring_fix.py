from zmatrix.regime_attribution.regime_separability_tester import test_regime_separability

def test_bull_bear_spread_triggers_weakly_separable():
    enriched = []
    for i in range(6000):
        enriched.append({"market_regime":"BULL_TREND","actual_return_t20":1,"invalidation_triggered":False})
    for i in range(6000):
        enriched.append({"market_regime":"BEAR_TREND","actual_return_t20":-1,"invalidation_triggered":True})
    performance = {"market_regime_profiles":{"BULL_TREND":{"count":25579,"win_rate":0.553,"median":1.24,"invalidation_rate":0.482},"BEAR_TREND":{"count":21441,"win_rate":0.406,"median":-2.10,"invalidation_rate":0.764},"RANGE_BOUND":{"count":53504,"win_rate":0.47,"median":-1.0,"invalidation_rate":0.67}}}
    r = test_regime_separability(enriched_rows=enriched, regime_performance_profile=performance)
    assert r["separability_status"] in ("WEAKLY_REGIME_SEPARABLE","REGIME_SEPARABLE")
    assert r["bull_bear_spread"]["win_rate_spread"] >= 0.10
    assert r["bull_bear_spread"]["median_spread"] >= 2.0
    assert r["bull_bear_spread"]["invalidation_spread"] >= 0.15
    assert "scoring_breakdown" in r
    assert r["real_trade_allowed"] is False
