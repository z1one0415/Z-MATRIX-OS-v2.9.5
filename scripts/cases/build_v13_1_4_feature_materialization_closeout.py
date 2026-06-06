#!/usr/bin/env python3
"""V13.1.4 Closeout — fail-closed, gated on materialization + validation + field gate."""
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_1_4_feature_materialization_contract.json");manifest=load("v13_1_4_materialized_feature_store_manifest.json")
    v=load("v13_1_4_materialized_feature_store_validation.json");fa=load("v13_1_candidate_field_availability_after_materialization.json")
    br=load("v13_1_bucket_readiness_after_materialization.json")
    mat_built="BUILT"in manifest.get("status","")
    val_ok="PASS"in v.get("status","")
    fa_ok="BLOCKED"not in fa.get("status","")and"BUILT"in fa.get("status","")
    ready=br.get("ready_candidate_count",0)if fa_ok else 0
    all_ok=mat_built and val_ok and fa_ok and ready>=4
    nxt="FIX_FEATURE_SOURCE_OR_MATERIALIZATION"if not mat_built else("FIX_REMAINING_FIELD_GAPS"if not val_ok or not fa_ok else"PREPARE_V13_2_BUCKET_CONSTRUCTION_IN_SEPARATE_STEP"if ready>=4 else"FIX_REMAINING_FIELD_GAPS")
    result={"status":"V13_1_4_FEATURE_MATERIALIZATION_CONFIRMED_READY_FOR_V13_1_FIELD_GATE_RERUN"if all_ok else"V13_1_4_FEATURE_MATERIALIZATION_CONFIRMED_BLOCKED",
        "materialized_feature_store_built":mat_built,"materialized_feature_store_validated":val_ok,"candidate_ready_after_materialization_count":ready,
        "ready_for_v13_1_field_gate_rerun":all_ok,"ready_for_v13_2_bucket_construction_next_stage":False,"v13_2_requires_separate_instruction":True,
        "alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","recommended_next_action":nxt}
    json.dump(result,open(C/"v13_1_4_feature_materialization_closeout.json","w"),indent=2)
    print(f"MatCloseout: {result['status']} built={mat_built} val={val_ok} ready={ready}")
if __name__=="__main__":main()
