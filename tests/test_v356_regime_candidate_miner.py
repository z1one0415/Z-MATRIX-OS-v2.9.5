from zmatrix.regime_attribution.regime_candidate_miner import mine_regime_candidates

def test_no_candidates_when_not_separable():
    r = mine_regime_candidates(separability={"separability_status":"NOT_REGIME_SEPARABLE"})
    assert r["candidate_count"] == 0
    assert r["real_trade_allowed"] is False
