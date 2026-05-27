from zmatrix.paper_repair_replay.invalidation_rule_extractor import extract_invalidation_rule

def test_extract_invalidation_rule_positive_loss():
    r = extract_invalidation_rule(action={"paper_id": "p1", "ticker": "000001", "max_loss_plan": 8})
    assert r["max_loss_pct"] == -8
    assert r["lookahead_safe"] is True
    assert r["real_trade_allowed"] is False
