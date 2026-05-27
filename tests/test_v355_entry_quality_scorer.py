from zmatrix.entry_quality_repair.entry_quality_scorer import score_entry_quality

def test_entry_quality_high():
    r = score_entry_quality(features={"price_above_ma20": True, "price_above_ma60": True, "return_20d": 8, "drawdown_from_20d_high": -3, "volatility_20d": 2, "volume_ratio_5_20": 1.2})
    assert r["entry_quality_score"] >= 65
    assert r["entry_quality_bucket"] == "HIGH_ENTRY_QUALITY"
    assert r["real_trade_allowed"] is False
