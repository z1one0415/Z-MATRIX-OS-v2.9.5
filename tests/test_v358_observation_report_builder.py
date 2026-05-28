from zmatrix.regime_observation.observation_report_builder import build_regime_observation_report

def test_observation_report_no_runtime():
    r = build_regime_observation_report(replay_report={}, anti_overfit_report={}, governance_report={})
    assert r["real_trade_allowed"] is False
    assert r["broker_order_allowed"] is False
    assert r["runtime_enabled"] is False
    assert r["production_yaml_write_allowed"] is False
    assert r["policy_violations"] == []
