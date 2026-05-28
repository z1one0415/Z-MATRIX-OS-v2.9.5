from zmatrix.regime_attribution.breadth_liquidity_builder import build_breadth_regime

def test_breadth_data_insufficient():
    r = build_breadth_regime()
    assert r["breadth_status"] == "DATA_INSUFFICIENT"
    assert r["real_trade_allowed"] is False
