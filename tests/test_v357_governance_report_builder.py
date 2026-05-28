from zmatrix.governance_closeout.governance_report_builder import build_governance_closeout_report

def test_governance_report_no_runtime():
    r = build_governance_closeout_report(regime_replay_report={"report_version":"test","full_sample_pass_policies":[]})
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["production_yaml_write_allowed"] is False
    assert r["policy_violations"] == []
