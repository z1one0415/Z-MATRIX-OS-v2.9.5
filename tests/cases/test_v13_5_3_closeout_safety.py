"""V13.5.3 Closeout Safety — targeted tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
co=L("v13_5_3_multi_rebalance_alpha_validation_closeout.json")
def test_exists():assert co
def test_executed():assert co.get("v13_5_3_executed")is True
def test_validation_mode():assert co.get("validation_mode")=="RESEARCH_ALPHA_EVIDENCE_ONLY"
def test_nxt_if_pass():
    if"PASS"in co.get("status",""):assert"PREPARE_V13_6"in co.get("recommended_next_action","")
def test_nxt_if_blocked():
    if"BLOCKED"in co.get("status",""):assert"IMPROVE_FACTORS"in co.get("recommended_next_action","")
def test_alpha_claim_false():assert co.get("alpha_claim_allowed")is False
def test_ready_for_alpha_false():assert co.get("ready_for_alpha_claim")is False
def test_alpha_validated_false():assert co.get("alpha_validated")is False
def test_prod_blocked():assert co.get("production")=="BLOCKED"
def test_broker_blocked():assert co.get("broker_runtime")=="BLOCKED"
def test_rt_blocked():assert co.get("real_trade")=="BLOCKED"
