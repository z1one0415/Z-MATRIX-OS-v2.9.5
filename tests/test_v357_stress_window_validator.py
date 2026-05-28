from zmatrix.regime_conditioned_replay.stress_window_validator import validate_stress_windows

def test_stress_windows():
    rows = [{"market_regime":"BEAR_TREND","actual_return_t20":-1,"regime_policy_action":"BLOCK"}]
    r = validate_stress_windows(rows=rows, policy_names=["test"])
    assert "test" in r["policy_results"]
