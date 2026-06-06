#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    reg=load("v13_1_candidate_registry.json");fa=load("v13_1_candidate_field_availability.json")
    lc=load("v13_1_label_coverage.json");us=load("v13_0_universe_eligibility_scan.json")
    fa_map={c["v13_1_candidate_run_id"]:c for c in fa.get("checks",[])}
    lc_map={c["v13_1_candidate_run_id"]:c for c in lc.get("checks",[])}
    items=[];ready=0;blkd=0
    for r in reg.get("registry_items",[]):
        rid=r["v13_1_candidate_run_id"];f=fa_map.get(rid,{});l=lc_map.get(rid,{})
        f_ok=f.get("field_availability_status")=="FIELDS_AVAILABLE"
        l_ok=l.get("label_coverage_status")=="FULL_COVERAGE"
        ok=f_ok and l_ok
        if ok:ready+=1
        else:blkd+=1
        reasons=[]
        if not f_ok:reasons.append("FIELD_MISSING")
        if not l_ok:reasons.append("LABEL_MISSING")
        items.append({"v13_1_candidate_run_id":rid,"factor_name":r["factor_name"],
            "field_availability_status":f.get("field_availability_status","UNKNOWN"),
            "label_coverage_status":l.get("label_coverage_status","UNKNOWN"),
            "eligible_ticker_count":us.get("eligible_ticker_count",70),
            "min_bucket_size":10,"max_bucket_imbalance":2,
            "bucket_readiness_status":"READY_FOR_BUCKET_CONSTRUCTION"if ok else"BLOCKED",
            "blocking_reasons":reasons})
    result={"status":"V13_1_BUCKET_READINESS_BUILT","candidate_count":len(items),
        "ready_for_bucket_construction_count":ready,"blocked_candidate_count":blkd,
        "readiness_items":items,"ready_for_v13_2_bucket_construction_next_stage":ready>=4,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_bucket_readiness.json","w"),indent=2)
    print(f"Readiness: {ready} ready, {blkd} blocked")
if __name__=="__main__":main()
