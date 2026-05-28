from zmatrix.governance_closeout.zg18_conflict_precheck import precheck_zg18_conflict_risk

def test_bull_only_conflict():
    r = precheck_zg18_conflict_risk(policies=["allow_b_rotation_in_bull_trend_only"])
    assert r["conflict_precheck_status"] == "CONFLICT_RISK_WARNING"
    assert r["g18_conflict_resolver_write_allowed"] is False
