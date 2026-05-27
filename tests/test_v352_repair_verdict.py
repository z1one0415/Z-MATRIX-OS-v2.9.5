from zmatrix.strategy_repair.repair_verdict import judge_repair_candidate

def test_repair_verdict_rejects_lookahead():
    r = judge_repair_candidate(candidate={"rule": {"lookahead_risk": True}, "kept_count": 2000, "metrics": {"top_1pct_contribution": 0.3}, "delta": {"win_rate_delta": 0.05, "median_delta": 0.5}})
    assert r["status"] == "REPAIR_CANDIDATE_REJECTED"
    assert "LOOKAHEAD_RISK" in r["reasons"]
