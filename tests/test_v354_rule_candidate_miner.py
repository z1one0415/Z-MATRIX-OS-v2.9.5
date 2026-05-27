from zmatrix.invalidation_anatomy.rule_candidate_miner import mine_conditional_invalidation_candidates

def test_no_candidates_when_not_separable():
    r = mine_conditional_invalidation_candidates(separability_report={"separability_status": "NOT_SEPARABLE"})
    assert r["candidate_count"] == 0
    assert r["real_trade_allowed"] is False
