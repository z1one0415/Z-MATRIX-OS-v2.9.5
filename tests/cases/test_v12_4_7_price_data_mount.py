"""V12.4.7: Price Data Mount Tests."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;assert p.exists();return json.loads(p.read_text())
def test_contract_5fields():assert len(load("v12_4_7_price_data_mount_contract.json")["required_fields"])==5
def test_discovery_checked():
    d=load("v12_4_7_price_data_file_discovery.json");assert d["candidates_checked"]==2;assert d["price_file_discovered"]is False
def test_schema_requires_adjusted_close():
    sv=load("v12_4_7_price_data_schema_validation.json")
    for v in sv.get("validations",[]):
        if v["schema_validation_status"]!="SCHEMA_BLOCKED":assert v["has_adjusted_close_column"]is True
def test_schema_requires_volume():
    sv=load("v12_4_7_price_data_schema_validation.json")
    for v in sv.get("validations",[]):
        if v["schema_validation_status"]!="SCHEMA_BLOCKED":assert v["has_volume_column"]is True
def test_coverage_requires_600837():
    tc=load("v12_4_7_price_data_target_coverage.json")
    for v in tc.get("validations",[]):
        if v["coverage_validation_status"]=="COVERAGE_PASS":assert v["target_ticker"]=="600837"
def test_audit_pass_no_file():
    a=load("v12_4_7_price_data_mount_audit.json");assert"PASS"in a["status"];assert a["ready_for_label_regeneration"]is False
def test_closeout_waiting():
    c=load("v12_4_7_price_data_mount_closeout.json");assert"WAITING"in c["status"];assert c["recommended_next_action"]=="MOUNT_VALID_PRICE_DATA_FILE"
def test_fc_pass():assert"PASS"in load("v12_4_7_price_data_mount_full_chain.json")["status"]
def test_fc_cycle2_blocked():assert load("v12_4_7_price_data_mount_full_chain.json")["cycle2_still_blocked"]is True
def test_fc_v12_5_blocked():assert load("v12_4_7_price_data_mount_full_chain.json")["v12_5_still_blocked"]is True
def test_fc_no_lr():assert load("v12_4_7_price_data_mount_full_chain.json")["ready_for_label_regeneration"]is False
