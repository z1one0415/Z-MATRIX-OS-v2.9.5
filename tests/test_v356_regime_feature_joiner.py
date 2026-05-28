from zmatrix.regime_attribution.regime_feature_joiner import join_regime_features

def test_join_regime_features():
    sample={"paper_id":"p1","ticker":"000001","entry_date":"20240101","actual_return_t20":5,"invalidation_triggered":False}
    mr={"regime":"BULL_TREND","all_regimes":["BULL_TREND"],"regime_data_status":"READY"}
    sp={"phase":"UNKNOWN_SECTOR_PHASE","sector_data_status":"DATA_INSUFFICIENT"}
    br={"breadth_regime":"UNKNOWN","liquidity_regime":"UNKNOWN","volatility_regime":"UNKNOWN","breadth_status":"DATA_INSUFFICIENT"}
    r = join_regime_features(sample=sample, market_regime=mr, sector_phase=sp, breadth=br, feature_status="PARTIAL")
    assert r["market_regime"] == "BULL_TREND"
    assert r["uses_future_data"] is False
    assert r["real_trade_allowed"] is False
