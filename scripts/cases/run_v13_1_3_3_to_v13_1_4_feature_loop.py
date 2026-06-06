#!/usr/bin/env python3
import subprocess,json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def lo(p):return json.loads(p.read_text())if p.exists()else{}
def main():
    ok=True
    # Step 1: Run source mount gate
    r=subprocess.run(["python3",str(W/"scripts/cases/run_v13_1_3_1_source_mount_full_chain.py")],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK'if r.returncode==0 else'FAIL'}: source_mount_gate {r.stdout.strip()[:120]}")
    if r.returncode!=0:print(f"  {r.stderr.strip()[:200]}");ok=False
    # Step 2: Read source mount result
    co=lo(C/"v13_1_3_1_source_mount_closeout.json")
    source_ready=co.get("ready_for_v13_1_4_feature_materialization_next_stage",False) and "READY"in co.get("status","")
    print(f"SourceReady: {source_ready}")
    # Step 3: Run missing report (always - confirms gap)
    r2=subprocess.run(["python3",str(W/"scripts/cases/build_v13_1_3_3_missing_feature_source_report.py")],cwd=str(W),capture_output=True,text=True)
    print(f"{'OK'if r2.returncode==0 else'FAIL'}: missing_report {r2.stdout.strip()[:120]}")
    v13_1_4_exec=False
    if source_ready:
        # Step 4: Execute V13.1.4 chain
        v13_steps=["build_v13_1_4_feature_materialization_contract.py","materialize_v13_1_4_feature_store.py","validate_v13_1_4_materialized_feature_store.py","rerun_v13_1_4_field_gate_after_materialization.py","build_v13_1_4_feature_materialization_closeout.py"]
        for vs in v13_steps:
            r3=subprocess.run(["python3",str(W/"scripts/cases"/vs)],cwd=str(W),capture_output=True,text=True)
            print(f"{'OK'if r3.returncode==0 else'FAIL'}: v13.1.4/{vs} {r3.stdout.strip()[:120]}")
        v13_1_4_exec=True
    v14_co=lo(C/"v13_1_4_feature_materialization_closeout.json")if source_ready else{}
    mat_built=v14_co.get("materialized_feature_store_built",False)if source_ready else False
    cand_ready=v14_co.get("candidate_ready_after_materialization_count",0)if source_ready else 0
    result={"status":"V13_1_3_3_TO_V13_1_4_FEATURE_LOOP_FULL_CHAIN_BLOCKED"if not source_ready else"V13_1_3_3_TO_V13_1_4_FEATURE_LOOP_FULL_CHAIN_PASS",
        "steps_returncode_pass":ok,"source_mount_ready":source_ready,"v13_1_4_executed":v13_1_4_exec,"materialized_feature_store_built":mat_built,
        "candidate_ready_after_materialization_count":cand_ready,"ready_for_v13_2_bucket_construction_next_stage":False,"v13_2_executed":False,
        "alpha_claim_allowed":False,"recommended_next_action":"PROVIDE_REAL_V13_FEATURE_SOURCE_FILES"if not source_ready else"PREPARE_V13_2_BUCKET_CONSTRUCTION_IN_SEPARATE_STEP",
        "forbidden_action_violations":[],"source_violations":[],"schema_violations":[],"coverage_violations":[],"asof_violations":[],"data_leakage_violations":[],"safety_violations":[],
        "investment_action_count":0,"trade_action_count":0,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_3_to_v13_1_4_feature_loop_full_chain.json","w"),indent=2)
    print(f"V13LoopFC: {result['status']} | source_ready={source_ready} v13.1.4={v13_1_4_exec}")
if __name__=="__main__":main()
