#!/usr/bin/env python3
"""V13.1.4 Field Gate — reads validator per_candidate_validation_status, never self-computes column readiness."""
import json,os;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    fd=os.environ.get("V13_FIXTURE_DIR","")
    pfx=Path(fd).name+"_"if fd else""
    vpath=f"fixtures/{pfx}feature_store_validation.json"if fd else"v13_1_4_materialized_feature_store_validation.json"
    manifest=json.loads((C/(f"fixtures/{pfx}feature_store_manifest.json"if fd else"v13_1_4_materialized_feature_store_manifest.json")).read_text())
    v=load(vpath)
    pc=v.get("per_candidate_validation_status",[])
    ready=[c for c in pc if c.get("candidate_validation_status")=="FEATURE_VALUES_VALIDATED"]
    n_ready=len(ready);n_miss=len(pc)-n_ready
    if v.get("status")=="V13_1_4_MATERIALIZED_FEATURE_STORE_VALIDATION_PASS":
        fa={"status":"V13_1_FIELD_GATE_AFTER_MATERIALIZATION_BUILT","candidate_count":len(pc),"fields_available_candidate_count":n_ready,"fields_missing_candidate_count":n_miss,
            "field_gate_source":"v13_1_4_materialized_feature_store_validation.per_candidate_validation_status","ready_for_v13_2_bucket_construction_next_stage":n_ready>=4,
            "v13_2_requires_separate_approval":True,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
        br={"status":"V13_1_BUCKET_READINESS_AFTER_MATERIALIZATION_BUILT","candidate_count":len(pc),"ready_candidate_count":n_ready,"blocked_candidate_count":n_miss}
    else:
        fa={"status":"V13_1_FIELD_GATE_AFTER_MATERIALIZATION_BLOCKED","candidate_count":len(pc),"fields_available_candidate_count":0,"fields_missing_candidate_count":len(pc),
            "field_gate_source":"v13_1_4_materialized_feature_store_validation.per_candidate_validation_status","blocked_reasons":v.get("blocking_reasons",["VALIDATION_NOT_PASS"]),
            "ready_for_v13_2_bucket_construction_next_stage":False,"v13_2_requires_separate_approval":True,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
        br={"status":"V13_1_BUCKET_READINESS_AFTER_MATERIALIZATION_BLOCKED","candidate_count":len(pc),"ready_candidate_count":0,"blocked_reasons":v.get("blocking_reasons",["VALIDATION_NOT_PASS"])}
    out_dir=C/"fixtures"if fd else C
    out_dir.mkdir(parents=True,exist_ok=True)
    json.dump(fa,open(out_dir/f"{pfx}candidate_field_availability_after_materialization.json","w"),indent=2)
    json.dump(br,open(out_dir/f"{pfx}bucket_readiness_after_materialization.json","w"),indent=2)
    print(f"FieldGate: {fa['status']} ready={n_ready}")
if __name__=="__main__":main()
