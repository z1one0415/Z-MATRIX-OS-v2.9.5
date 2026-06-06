#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    sv=load("v13_1_3_1_strict_source_schema_validation.json");cv=load("v13_1_3_1_strict_coverage_validation.json")
    av=load("v13_1_3_1_strict_asof_validation.json")
    items=[];mv=0;mb=0;ns=0
    for i in range(len(sv.get("validations",[]))):
        g=sv["validations"][i]["feature_group"];s=sv["validations"][i].get("schema_status","")
        c=cv["validations"][i].get("coverage_status","");a=av["validations"][i].get("asof_status","")
        if s=="SCHEMA_PASS"and c=="COVERAGE_PASS"and a=="ASOF_PASS":dec="MOUNT_VALIDATED";mv+=1
        elif s=="NO_SOURCE":dec="NO_SOURCE";ns+=1
        else:dec="MOUNT_BLOCKED";mb+=1
        items.append({"feature_group":g,"schema_status":s,"coverage_status":c,"asof_status":a,"mount_decision":dec})
    ready=mv>=4
    result={"status":"V13_1_3_1_MOUNT_DECISION_BUILT","feature_group_count":5,"mount_validated_group_count":mv,"mount_blocked_group_count":mb,"no_source_group_count":ns,"mount_decisions":items,"ready_for_v13_1_4_feature_materialization_next_stage":ready,"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_mount_decision.json","w"),indent=2)
    print(f"Decision: {mv}v/{mb}b/{ns}ns ready={ready}")
if __name__=="__main__":main()
