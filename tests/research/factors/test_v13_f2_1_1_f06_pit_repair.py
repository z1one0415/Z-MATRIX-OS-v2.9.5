"""V13.F2.1.1 — F06 PIT repair tests."""
import json,csv;from pathlib import Path
from tests._path_utils import RUNTIME_FACTORS
def L(p):return json.loads((RUNTIME_FACTORS/p).read_text())if(RUNTIME_FACTORS/p).exists()else{}
f06_m=L("f06_fundamental_quality_materialization.json")
audit=L("f06_pit_null_row_audit.json")
co11=L("v13_f2_1_1_f06_pit_repair_closeout.json")
def test_no_null_known():assert f06_m.get("null_known_at_row_count",99)==0
def test_no_placeholder():assert f06_m.get("placeholder_zero_row_count",99)==0
def test_pit_pass():assert f06_m.get("known_at_pass")is True
def test_audit_pass():assert audit.get("pit_null_audit_passed")is True
def test_validated_2():assert co11.get("validated_factor_count")==2
def test_no_ic():assert co11.get("ic_validation_executed")is False
def test_no_alpha():assert co11.get("alpha_claim_allowed")is False
def test_no_v13_6():assert co11.get("v13_6_allowed")is False
def test_prod():assert f06_m.get("production")=="BLOCKED"
