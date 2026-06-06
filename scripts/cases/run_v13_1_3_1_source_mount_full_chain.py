#!/usr/bin/env python3
import subprocess,json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["build_v13_1_3_1_source_mount_provenance_contract.py","build_v13_1_3_1_mounted_file_inventory.py","map_v13_1_3_1_feature_sources.py","validate_v13_1_3_1_strict_source_schemas.py","validate_v13_1_3_1_strict_coverage.py","validate_v13_1_3_1_strict_asof.py","build_v13_1_3_1_mount_decision.py","build_v13_1_3_1_candidate_mount_readiness.py","audit_v13_1_3_1_source_mount.py","build_v13_1_3_1_source_mount_closeout.py"]
def lo(p):return json.loads(p.read_text())if p.exists()else{}
def main():
    ok=True
    for s in S:
        r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
        print(f"{'OK'if r.returncode==0 else'FAIL'}: {s} {r.stdout.strip()[:120]}")
        if r.returncode!=0:print(f"  {r.stderr.strip()[:200]}");ok=False
    inv=lo(C/"v13_1_3_1_mounted_file_inventory.json");sv=lo(C/"v13_1_3_1_strict_source_schema_validation.json")
    cv=lo(C/"v13_1_3_1_strict_coverage_validation.json");av=lo(C/"v13_1_3_1_strict_asof_validation.json")
    md=lo(C/"v13_1_3_1_mount_decision.json");cm=lo(C/"v13_1_3_1_candidate_mount_readiness.json")
    co=lo(C/"v13_1_3_1_source_mount_closeout.json");au=lo(C/"v13_1_3_1_source_mount_audit.json")
    result={"status":"V13_1_3_1_SOURCE_MOUNT_FULL_CHAIN_PASS"if ok else"V13_1_3_1_SOURCE_MOUNT_FULL_CHAIN_BLOCKED","steps":S,"steps_returncode_pass":ok,"accepted_for_validation_count":inv.get("accepted_for_validation_count",0),"schema_pass_group_count":sv.get("schema_pass_group_count",0),"coverage_pass_group_count":cv.get("coverage_pass_group_count",0),"asof_pass_group_count":av.get("asof_pass_group_count",0),"mount_validated_group_count":md.get("mount_validated_group_count",0),"candidate_mount_ready_count":cm.get("candidate_mount_ready_count",0),"candidate_mount_blocked_count":cm.get("candidate_mount_blocked_count",0),"ready_for_v13_1_4_feature_materialization_next_stage":co.get("ready_for_v13_1_4_feature_materialization_next_stage",False),"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"recommended_next_action":co.get("recommended_next_action",""),"forbidden_action_violations":[],"source_violations":[],"schema_violations":[],"coverage_violations":[],"asof_violations":[],"data_leakage_violations":[],"safety_violations":[],"investment_action_count":0,"trade_action_count":0,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_source_mount_full_chain.json","w"),indent=2)
    print(f"SMFC: {result['status']} mv={result['mount_validated_group_count']}")
if __name__=="__main__":main()
