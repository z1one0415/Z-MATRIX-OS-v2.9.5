"""V13.1.1 Field Availability Tests"""
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;assert p.exists();return json.loads(p.read_text())
def test_registry_8():assert load("v13_1_candidate_registry.json")["registered_candidate_count"]==8
def test_event_clean_excluded():assert"EVENT_CLEAN_REL_STRENGTH"in load("v13_1_candidate_registry.json")["excluded_candidates"]
def test_registry_has_definitions():
    for r in load("v13_1_candidate_registry.json")["registry_items"]:assert r["factor_definition"];assert r["factor_definition_hash"]
def test_field_not_all_empty():
    fa=load("v13_1_candidate_field_availability.json");assert fa["candidates_with_empty_required_fields"]==0
def test_field_has_missing():
    fa=load("v13_1_candidate_field_availability.json")
    # At least some candidates should have non-empty required fields identified
    has_req=sum(1 for c in fa["checks"]if c["required_fields"])
    assert has_req>0,f"All candidates have empty required_fields"
def test_missing_fields_block_readiness():
    br=load("v13_1_bucket_readiness.json");fa=load("v13_1_candidate_field_availability.json")
    fa_map={c["v13_1_candidate_run_id"]:c for c in fa["checks"]}
    for b in br["readiness_items"]:
        f=fa_map.get(b["v13_1_candidate_run_id"],{})
        if f.get("field_availability_status")=="FIELDS_MISSING":assert b["bucket_readiness_status"]=="BLOCKED"
def test_label_coverage_has_data():lc=load("v13_1_label_coverage.json");assert"600837"in lc["excluded_tickers"]
def test_fc_safety():
    fc=load("v13_1_paper_bootstrap_full_chain.json")
    assert fc["ready_for_alpha_claim"]is False;assert fc["alpha_validated"]is False
    assert fc["alpha_claim_allowed"]is False;assert fc["production"]=="BLOCKED"
    assert fc["broker_runtime"]=="BLOCKED";assert fc["real_trade"]=="BLOCKED"
