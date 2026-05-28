from zmatrix.regime_observation.temporal_instability_attributor import attribute_temporal_instability

def test_temporal_instability_empty():
    r = attribute_temporal_instability(anti_overfit_report={"per_policy_validation":{}})
    assert r["attribution_version"]

def test_temporal_instability_with_windows():
    r = attribute_temporal_instability(anti_overfit_report={"per_policy_validation":{"test":{"temporal":{"temporal_status":"TEMPORAL_INSTABILITY","windows":[{"year":"2024","baseline_win":0.4,"policy_win":0.5,"win_delta":0.1,"baseline_median":-2,"policy_median":0,"median_delta":2,"pass":True}]}}}})
    assert "test" in r["policy_temporal_results"]
