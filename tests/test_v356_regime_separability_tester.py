from zmatrix.regime_attribution.regime_separability_tester import test_regime_separability

def test_regime_separability_data_insufficient():
    r = test_regime_separability(enriched_rows=[])
    assert r["separability_status"] == "DATA_INSUFFICIENT"
    assert r["real_trade_allowed"] is False
