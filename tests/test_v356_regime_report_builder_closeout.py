from zmatrix.regime_attribution.regime_report_builder import build_regime_attribution_report

def test_regime_report_contains_closeout_fields():
    r = build_regime_attribution_report(joined=[{"paper_id":"p1","ticker":"000001","entry_date":"20240101","role":"B_MID_ROTATION","actual_return_t20":-2,"invalidation_triggered":True}], index_data={}, max_items=1)
    assert "regime_scoring_breakdown" in r
    assert "bull_bear_spread" in r
    assert "recommended_next_step" in r
    assert r["policy_violations"] == []
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
