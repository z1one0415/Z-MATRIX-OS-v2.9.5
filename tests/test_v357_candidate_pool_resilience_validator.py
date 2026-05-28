from zmatrix.governance_closeout.candidate_pool_resilience_validator import validate_candidate_pool_resilience

def test_low_kept_rate_blocked():
    r = validate_candidate_pool_resilience(policy_results={"test":{"kept_count":10,"original_count":100,"kept_rate":0.1,"kept_rows":[{"entry_date":"20240101"}]*10}})
    assert "test" in r["policy_pool_results"]
    assert r["policy_pool_results"]["test"]["pool_resilience_status"] == "POOL_RESILIENCE_BLOCKED"

def test_concentrated_risk():
    r = validate_candidate_pool_resilience(policy_results={"test":{"kept_count":30,"original_count":100,"kept_rate":0.3,"kept_rows":[{"entry_date":"20240101"}]*3}})
    assert r["policy_pool_results"]["test"]["pool_resilience_status"] == "POOL_RESILIENCE_WARNING"
