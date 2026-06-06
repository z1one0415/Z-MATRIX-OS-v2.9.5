"""V13.1.3.3 Conditional Loop Tests"""
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;assert p.exists();return json.loads(p.read_text())
def test_loop_not_executed_when_source_not_ready():assert load("v13_1_3_3_to_v13_1_4_feature_loop_full_chain.json")["v13_1_4_executed"]is False
def test_v13_2_not_ready():assert load("v13_1_3_3_to_v13_1_4_feature_loop_full_chain.json")["ready_for_v13_2_bucket_construction_next_stage"]is False
def test_v13_2_not_executed():assert load("v13_1_3_3_to_v13_1_4_feature_loop_full_chain.json")["v13_2_executed"]is False
def test_safety():
    fc=load("v13_1_3_3_to_v13_1_4_feature_loop_full_chain.json")
    assert fc["alpha_claim_allowed"]is False;assert fc["ready_for_alpha_claim"]is False;assert fc["alpha_validated"]is False
    assert fc["production"]=="BLOCKED";assert fc["broker_runtime"]=="BLOCKED";assert fc["real_trade"]=="BLOCKED"
