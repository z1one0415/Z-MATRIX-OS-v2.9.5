"""V13.0 Tests"""
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;assert p.exists();return json.loads(p.read_text())
def test_contract_v12_closed():assert load("v13_0_research_restart_contract.json")["v12_research_loop_closed"]is True
def test_freeze_hit_zero():assert load("v13_0_v12_failure_freeze_manifest.json")["total_hit_count"]==0
def test_freeze_miss_12():assert load("v13_0_v12_failure_freeze_manifest.json")["total_miss_count"]==12
def test_freeze_12_factors():assert len(load("v13_0_v12_failure_freeze_manifest.json")["frozen_factors"])==12
def test_denylist_12():assert load("v13_0_failed_seed_denylist.json")["denylist_count"]==12
def test_denylist_no_reuse():assert load("v13_0_failed_seed_denylist.json")["direct_reuse_allowed_count"]==0
def test_universe_600837_ineligible():
    it=[i["ticker"]for i in load("v13_0_universe_eligibility_scan.json")["ineligible_tickers"]];assert"600837"in it
def test_discovery_no_reuse():assert load("v13_0_candidate_discovery_contract.json")["failed_seed_reuse_blocked"]is True
def test_pool_has_candidates():assert load("v13_0_new_candidate_pool.json")["accepted_candidate_count"]>=4
def test_pool_each_has_hyp():
    for c in load("v13_0_new_candidate_pool.json")["candidates"]:
        if not c.get("denied_by_denylist"):assert c["hypothesis_id"]
def test_pool_each_has_hash():
    for c in load("v13_0_new_candidate_pool.json")["candidates"]:
        if not c.get("denied_by_denylist"):assert c["factor_definition_hash"]
def test_pool_no_reuse_violation():assert load("v13_0_new_candidate_pool.json")["failed_seed_reuse_violation_count"]==0
def test_quality_gate_pass():assert"PASS"in load("v13_0_candidate_quality_gate_audit.json")["status"]
def test_closeout_alpha_false():assert load("v13_0_research_restart_closeout.json")["alpha_claim_allowed"]is False
def test_fc_pass():assert"PASS"in load("v13_0_research_restart_full_chain.json")["status"]
def test_fc_safety():
    fc=load("v13_0_research_restart_full_chain.json")
    assert fc["ready_for_alpha_claim"]is False;assert fc["alpha_validated"]is False
    assert fc["production"]=="BLOCKED";assert fc["broker_runtime"]=="BLOCKED";assert fc["real_trade"]=="BLOCKED"
    assert fc["investment_action_count"]==0;assert fc["trade_action_count"]==0
