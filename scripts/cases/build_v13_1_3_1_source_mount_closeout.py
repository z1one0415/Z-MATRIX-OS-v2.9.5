#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    md=load("v13_1_3_1_mount_decision.json");cm=load("v13_1_3_1_candidate_mount_readiness.json")
    mv=md.get("mount_validated_group_count",0);cr=cm.get("candidate_mount_ready_count",0)
    ready=mv>=4 and cr>=4
    nxt="V13_1_4_MATERIALIZE_FEATURE_STORE_AND_RERUN_FIELD_GATE"if ready else"MOUNT_MISSING_V13_FEATURE_SOURCES"
    result={"status":"V13_1_3_1_SOURCE_MOUNT_CONFIRMED_READY_FOR_MATERIALIZATION"if ready else"V13_1_3_1_SOURCE_MOUNT_CONFIRMED_BLOCKED","source_mount_gate_confirmed":True,"mount_validated_group_count":mv,"candidate_mount_ready_count":cr,"ready_for_v13_1_4_feature_materialization_next_stage":ready,"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","recommended_next_action":nxt}
    json.dump(result,open(C/"v13_1_3_1_source_mount_closeout.json","w"),indent=2)
    print(f"Closeout: {'READY' if ready else 'BLOCKED'} mv={mv} cr={cr}")
if __name__=="__main__":main()
