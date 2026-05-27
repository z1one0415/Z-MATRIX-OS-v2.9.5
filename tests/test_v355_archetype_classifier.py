from zmatrix.entry_quality_repair.b_rotation_archetype_classifier import classify_b_rotation_archetype

def test_downtrend_bounce_trap_archetype():
    r = classify_b_rotation_archetype(features={"return_20d": -15, "drawdown_from_20d_high": -18, "volatility_20d": 3, "volume_ratio_5_20": 1, "price_above_ma20": False, "price_above_ma60": False})
    assert r["archetype"] == "DOWNTREND_BOUNCE_TRAP"
    assert r["real_trade_allowed"] is False
