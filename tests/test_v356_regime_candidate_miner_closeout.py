from zmatrix.regime_attribution.regime_candidate_miner import mine_regime_candidates

def test_regime_candidates_generated_when_weakly_separable():
    r = mine_regime_candidates(separability={"separability_status":"WEAKLY_REGIME_SEPARABLE"})
    names = [c["candidate_name"] for c in r["candidates"]]
    assert "block_b_rotation_in_bear_trend" in names
    assert "allow_b_rotation_in_bull_trend_only" in names
    assert "require_non_bear_market" in names
    assert all(c["lookahead_risk"] is False for c in r["candidates"])
    assert all(c["production_ready"] is False for c in r["candidates"])
    assert r["real_trade_allowed"] is False

def test_no_regime_candidates_when_not_separable():
    r = mine_regime_candidates(separability={"separability_status":"NOT_REGIME_SEPARABLE"})
    assert r["candidate_count"] == 0
    assert r["candidates"] == []
