from zmatrix.regime_attribution.regime_report_builder import build_regime_attribution_report

def test_regime_report_no_runtime():
    r = build_regime_attribution_report(joined=[{"paper_id":"p1","ticker":"000001","entry_date":"20240101","role":"B_MID_ROTATION","actual_return_t20":-2,"invalidation_triggered":True}], index_data={}, max_items=1)
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
