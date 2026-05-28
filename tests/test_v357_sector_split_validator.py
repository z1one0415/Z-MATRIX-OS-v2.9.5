from zmatrix.regime_conditioned_replay.sector_split_validator import validate_sector_stability

def test_sector_data_insufficient():
    rows = [{"actual_return_t20":1,"regime_policy_action":"KEEP"}]
    r = validate_sector_stability(rows=rows, policy_names=["test"])
    assert r["sector_status"] == "DATA_INSUFFICIENT"
