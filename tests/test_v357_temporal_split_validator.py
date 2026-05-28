from zmatrix.regime_conditioned_replay.temporal_split_validator import validate_temporal_stability

def test_temporal_insufficient_windows():
    rows = [{"entry_date":"20240101","actual_return_t20":1,"regime_policy_action":"KEEP"}]
    r = validate_temporal_stability(rows=rows, policy_names=["test"])
    assert r["temporal_validation_version"]
