"""V13.0.2 Tests"""
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;assert p.exists();return json.loads(p.read_text())
def test_archive_5():assert load("v13_0_2_rejected_candidate_archive.json")["rejected_count"]==5
def test_pool_preserved():assert load("v13_0_2_redesigned_candidate_pool.json")["preserved_candidate_count"]==3
def test_pool_new():assert load("v13_0_2_redesigned_candidate_pool.json")["new_candidate_count"]>=5
def test_pool_total():assert load("v13_0_2_redesigned_candidate_pool.json")["candidate_count"]>=8
def test_overlap_reject_zero():assert load("v13_0_2_redesigned_candidate_overlap_scorecard.json")["reject_as_reuse_count"]==0
def test_overlap_pass():assert load("v13_0_2_redesigned_candidate_overlap_scorecard.json")["pass_overlap_count"]>=6
def test_quality_pass():assert"PASS"in load("v13_0_2_redesigned_candidate_quality_audit.json")["status"]
def test_quality_accepted():assert load("v13_0_2_redesigned_candidate_quality_audit.json")["accepted_for_v13_1_count"]>=6
def test_quality_no_reentry():assert load("v13_0_2_redesigned_candidate_quality_audit.json")["archived_rejected_reentry_count"]==0
def test_closeout_confirmed():assert"CONFIRMED"in load("v13_0_2_redesigned_candidate_closeout.json")["status"]
def test_fc_pass():assert"PASS"in load("v13_0_2_redesigned_candidate_full_chain.json")["status"]
def test_fc_safety():
    fc=load("v13_0_2_redesigned_candidate_full_chain.json")
    assert fc["ready_for_alpha_claim"]is False;assert fc["alpha_validated"]is False
    assert fc["alpha_claim_allowed"]is False;assert fc["production"]=="BLOCKED"
    assert fc["broker_runtime"]=="BLOCKED";assert fc["real_trade"]=="BLOCKED"
