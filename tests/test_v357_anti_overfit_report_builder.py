from zmatrix.regime_conditioned_replay.anti_overfit_report_builder import build_anti_overfit_report

def test_anti_overfit_report_no_runtime():
    rows = [{"entry_date":"20240101","market_regime":"BULL_TREND","actual_return_t20":1,"regime_policy_action":"KEEP"}]*100
    r = build_anti_overfit_report(rows=rows, full_sample_policies=["test"])
    assert r["production_strategy_modified"] is False
    assert r["real_trade_allowed"] is False
    assert r["mode"] == "ANTI_OVERFIT_VALIDATION_ONLY"
