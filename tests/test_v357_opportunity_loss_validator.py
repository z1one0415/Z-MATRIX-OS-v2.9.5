from zmatrix.regime_conditioned_replay.opportunity_loss_validator import validate_opportunity_loss

def test_opportunity_loss_low_kept_rate():
    rows = [{"actual_return_t20":1,"regime_policy_action":"KEEP"}] + [{"actual_return_t20":1,"regime_policy_action":"BLOCK"}]*99
    r = validate_opportunity_loss(rows=rows, policy_names=["test"])
    assert r["policy_results"]["test"]["opportunity_loss_status"] == "LOW_KEPT_RATE_BLOCKED"
