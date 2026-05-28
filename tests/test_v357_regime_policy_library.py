from zmatrix.regime_conditioned_replay.regime_policy_library import apply_regime_policy

def test_block_bear_trend():
    rows = [{"market_regime":"BULL_TREND","actual_return_t20":5},{"market_regime":"BEAR_TREND","actual_return_t20":-3},{"market_regime":"RANGE_BOUND","actual_return_t20":1}]
    r = apply_regime_policy(rows=rows, policy_name="block_b_rotation_in_bear_trend")
    assert r["kept_count"] == 2
    assert all(row["market_regime"] != "BEAR_TREND" for row in r["kept"])
    assert r["real_trade_allowed"] is False

def test_bull_only():
    rows = [{"market_regime":"BULL_TREND","actual_return_t20":5},{"market_regime":"BEAR_TREND","actual_return_t20":-3}]
    r = apply_regime_policy(rows=rows, policy_name="allow_b_rotation_in_bull_trend_only")
    assert r["kept_count"] == 1
    assert r["kept"][0]["market_regime"] == "BULL_TREND"
