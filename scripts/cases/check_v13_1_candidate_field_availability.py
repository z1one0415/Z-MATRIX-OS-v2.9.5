#!/usr/bin/env python3
import json;from pathlib import Path
def load(n):p=Path("runtime_reports/cases")/n;return json.loads(p.read_text())if p.exists()else{}
AVAILABLE_REAL=["AMOUNT_20D_AVG","AMOUNT_60D_AVG","MOM_60D","TRAILING_BENCHMARK_RELATIVE_60D","VOLATILITY_20D","VOLATILITY_60D"]
def parse_required(defn,name):
    d=(defn+" "+name).lower();req=[]
    if any(w in d for w in["sector","industry_neutral","industry","sector-bucketed","sector_dispersion"]):req.append("sector_or_industry")
    if any(w in d for w in["drawdown","recovery","downside_vol","downside"]):req.append("drawdown_or_recovery")
    if"turnover"in d:req.append("turnover")
    if any(w in d for w in["rank_accel","rank_dynamics","short_rank","medium_rank"]):req.append("rank_short_medium")
    if any(w in d for w in["fundamental","quality_stability","fundamental_proxy","quality_proxy"]):req.append("fundamental_proxy_field")
    return req
def main():
    reg=load("v13_1_candidate_registry.json")
    items=[];fa=0;fm=0;empty_req=0
    for r in reg.get("registry_items",[]):
        req=parse_required(r.get("factor_definition",""),r["factor_name"])
        if not req and not r.get("is_new_candidate"):
            defn=r.get("factor_definition","").upper()
            if any(t in defn for t in AVAILABLE_REAL):req=["existing_V8_factor_fields"]
        missing=[f for f in req if f!="existing_V8_factor_fields"]
        if not req:empty_req+=1
        ok=len(req)>0 and len(missing)==0
        if ok:fa+=1
        else:fm+=1
        items.append({"v13_1_candidate_run_id":r["v13_1_candidate_run_id"],"factor_name":r["factor_name"],
            "required_fields":req,"available_fields":["v11_paper_snapshot_fields"]if req==["existing_V8_factor_fields"]else[],
            "missing_fields":missing,"field_availability_status":"FIELDS_AVAILABLE"if ok else"FIELDS_MISSING",
            "blocking_reasons":[]if ok else[f"MISSING_{f.upper()}"for f in missing]})
    result={"status":"V13_1_FIELD_AVAILABILITY_CHECK_BUILT","candidate_count":len(items),
        "fields_available_candidate_count":fa,"fields_missing_candidate_count":fm,
        "candidates_with_empty_required_fields":empty_req,"available_field_sources":["v11_paper_signal_snapshot"],
        "checks":items,"ready_for_bucket_construction_count":fa,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(Path("runtime_reports/cases")/"v13_1_candidate_field_availability.json","w"),indent=2)
    print(f"Fields: {fa} available, {fm} missing, {empty_req} empty-req")
if __name__=="__main__":main()
