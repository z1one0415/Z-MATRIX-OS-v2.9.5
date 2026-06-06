#!/usr/bin/env python3
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v12_4_7_price_data_mount_contract.json");disc=load("v12_4_7_price_data_file_discovery.json")
    sv=load("v12_4_7_price_data_schema_validation.json");tc=load("v12_4_7_price_data_target_coverage.json")
    audit=load("v12_4_7_price_data_mount_audit.json")
    ok=lambda d:"BUILT"in d.get("status","").upper()
    all_ok=all([ok(ct),ok(disc),ok(sv),ok(tc)])
    ap="PASS"in audit.get("status","")
    sf=all([ct.get("production")=="BLOCKED",ct.get("broker_runtime")=="BLOCKED",ct.get("real_trade")=="BLOCKED"])
    passed=all_ok and ap and sf
    mounted=audit.get("price_file_mounted",False)
    lr=audit.get("ready_for_label_regeneration",False)
    if lr:act="V12_4_8_REGENERATE_MISSING_FORWARD_LABEL_FROM_VALID_PRICE_DATA"
    else:act="MOUNT_VALID_PRICE_DATA_FILE"
    if not lr:status="V12_4_7_PRICE_DATA_MOUNT_CONFIRMED_WAITING_FOR_FILE"
    else:status="V12_4_7_PRICE_DATA_MOUNT_CONFIRMED_READY_FOR_LABEL_REGENERATION"
    result={"status":status,"price_data_mount_gate_confirmed":passed,
        "price_file_mounted":mounted,"schema_validated":audit.get("schema_validated",False),
        "target_coverage_ok":audit.get("target_coverage_ok",False),
        "ready_for_label_regeneration":lr,"cycle2_completion_status":"BLOCKED",
        "v12_5_feedback_allowed":False,"selected_price_file":tc.get("selected_price_file"),
        "recommended_next_action":act,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v12_4_7_price_data_mount_closeout.json","w"),indent=2)
    print(f"Closeout: {result['status']} | lr={lr}")
if __name__=="__main__":main()
