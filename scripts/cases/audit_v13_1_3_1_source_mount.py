#!/usr/bin/env python3
import json,re;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    inv=load("v13_1_3_1_mounted_file_inventory.json");sv=load("v13_1_3_1_strict_source_schema_validation.json")
    cv=load("v13_1_3_1_strict_coverage_validation.json");av=load("v13_1_3_1_strict_asof_validation.json")
    md=load("v13_1_3_1_mount_decision.json");cm=load("v13_1_3_1_candidate_mount_readiness.json")
    reasons=[];mv=md.get("mount_validated_group_count",0)
    if mv>sv.get("schema_pass_group_count",0):reasons.append("MANIFEST_VS_SCHEMA")
    blocked=len(reasons)>0
    result={"status":"V13_1_3_1_SOURCE_MOUNT_AUDIT_PASS"if not blocked else"V13_1_3_1_SOURCE_MOUNT_AUDIT_BLOCKED","source_mount_gate_confirmed":not blocked,"mount_validated_group_count":mv,"candidate_mount_ready_count":cm.get("candidate_mount_ready_count",0),"ready_for_v13_1_4_feature_materialization_next_stage":md.get("ready_for_v13_1_4_feature_materialization_next_stage",False),"ready_for_v13_2_bucket_construction_next_stage":False,"forbidden_action_violations":[],"investment_action_count":0,"trade_action_count":0,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_source_mount_audit.json","w"),indent=2)
    print(f"Audit: {result['status']} mv={mv}")
if __name__=="__main__":main()
