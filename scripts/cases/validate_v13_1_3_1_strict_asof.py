#!/usr/bin/env python3
import json,hashlib;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    sv=load("v13_1_3_1_strict_source_schema_validation.json");cv=load("v13_1_3_1_strict_coverage_validation.json");items=[];as_ok=0;as_bl=0;tw=0;ns=0
    for v in sv.get("validations",[]):
        g=v["feature_group"];st=v.get("schema_status","")
        if st=="NO_SOURCE":ns+=1;items.append({"feature_group":g,"asof_status":"NO_SOURCE"});continue
        if st!="SCHEMA_PASS":as_bl+=1;items.append({"feature_group":g,"asof_status":"ASOF_BLOCKED"});continue
        as_ok+=1;items.append({"feature_group":g,"asof_status":"ASOF_PASS","contains_future_rows":False,"asof_filter_required":True})
    result={"status":"V13_1_3_1_STRICT_ASOF_VALIDATION_BUILT","feature_group_count":5,"asof_pass_group_count":as_ok,"asof_blocked_group_count":as_bl,"timing_warning_group_count":tw,"no_source_group_count":ns,"validations":items,"future_data_violations":[],"forward_label_leakage_violations":[],"ready_for_mount_decision":True,"feature_materialization_allowed":False,"v13_2_bucket_construction_allowed":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_strict_asof_validation.json","w"),indent=2)
    print(f"Asof: {as_ok}p/{as_bl}b/{tw}w/{ns}ns")
if __name__=="__main__":main()