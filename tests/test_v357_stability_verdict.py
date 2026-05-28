from zmatrix.regime_conditioned_replay.stability_verdict import build_stability_verdict

def test_stability_blocks_overfit():
    temporal = {"policy_results":{"test":{"temporal_status":"TEMPORAL_INSTABILITY"}}}
    sector = {"policy_results":{"test":{"sector_status":"SECTOR_INSTABILITY"}}}
    stress = {"policy_results":{"test":{}}}
    opportunity = {"policy_results":{"test":{"opportunity_loss_status":"SAMPLE_RETENTION_OK","kept_rate":0.5}}}
    r = build_stability_verdict(full_sample_policies=["test"], temporal=temporal, sector=sector, stress=stress, opportunity=opportunity)
    assert r["verdicts"]["test"]["anti_overfit_status"] in ("TEMPORAL_INSTABILITY_BLOCKED","OVERFIT_RISK_BLOCKED")
    assert not r["verdicts"]["test"]["promotion_allowed"]
