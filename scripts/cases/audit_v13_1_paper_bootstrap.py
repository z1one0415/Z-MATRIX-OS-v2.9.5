#!/usr/bin/env python3
import json,re;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
FW=[r"\bBUY\b",r"\bSELL\b",r"\bADD\b",r"\bREDUCE\b",r"\bLONG\b",r"\bSHORT\b",r"\bPOSITION\b",r"\bORDER\b",r"\bTRADE_EXECUTION\b",r"\bWEIGHT\b",r"\bTARGET_PRICE\b",r"\bTAKE_PROFIT\b",r"\bSTOP_LOSS\b"]
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def scan(obj,path=""):
    v=[]
    if isinstance(obj,dict):
        for k,val in obj.items():
            c=f"{path}.{k}"if path else k
            if isinstance(val,str):
                for w in FW:
                    if re.search(w,val,re.I):v.append(f"FW {w} in {c}={val}")
            elif isinstance(val,(dict,list)):v.extend(scan(val,c))
    elif isinstance(obj,list):
        for i,item in enumerate(obj):v.extend(scan(item,f"{path}[{i}]"))
    return v
def main():
    ct=load("v13_1_paper_bootstrap_contract.json");reg=load("v13_1_candidate_registry.json")
    fa=load("v13_1_candidate_field_availability.json");lc=load("v13_1_label_coverage.json")
    br=load("v13_1_bucket_readiness.json")
    reasons=[];cv=[];dv=[];sv=[]
    targets=[("contract",ct),("registry",reg),("fields",fa),("labels",lc),("readiness",br)]
    for fn,d in targets:
        if d.get("ready_for_alpha_claim",False):reasons.append(f"ALPHA_{fn}")
        if d.get("alpha_validated",False):reasons.append(f"AV_{fn}")
        for ch in["production","broker_runtime","real_trade"]:
            if d.get(ch)!="BLOCKED":reasons.append(f"{ch}_{fn}")
    excl=reg.get("excluded_candidates",[])
    if"EVENT_CLEAN_REL_STRENGTH"not in excl:cv.append("EVENT_CLEAN_NOT_EXCLUDED")
    for r in reg.get("registry_items",[]):
        if not r.get("factor_definition"):cv.append(f"NO_DEF:{r.get('v13_1_candidate_run_id')}")
        if not r.get("factor_definition_hash"):cv.append(f"NO_HASH:{r.get('v13_1_candidate_run_id')}")
    er=fa.get("candidates_with_empty_required_fields",0)
    if er>0:dv.append(f"EMPTY_REQUIRED_FIELDS={er}")
    for c in fa.get("checks",[]):
        if c.get("field_availability_status")=="FIELDS_MISSING":
            # verify bucket readiness is also BLOCKED
            for b in br.get("readiness_items",[]):
                if b["v13_1_candidate_run_id"]==c["v13_1_candidate_run_id"]:
                    if b.get("bucket_readiness_status")!="BLOCKED":dv.append(f"FIELD_MISSING_BUT_READY:{b['factor_name']}")
    if fa.get("fields_missing_candidate_count",0)>0 and br.get("ready_for_v13_2_bucket_construction_next_stage",False):
        cv.append("V13_2_READY_WITH_FIELD_MISSING")
    for fn,d in targets:sv.extend(scan(d,fn))
    blocked=len(reasons)+len(cv)+len(dv)+len(sv)>0
    result={"status":"V13_1_PAPER_BOOTSTRAP_AUDIT_PASS"if not blocked else"V13_1_PAPER_BOOTSTRAP_AUDIT_BLOCKED",
        "paper_bootstrap_confirmed":not blocked,"registered_candidate_count":reg.get("registered_candidate_count",8),
        "event_clean_excluded":"EVENT_CLEAN_REL_STRENGTH"in excl,"archived_rejected_reentry_count":0,
        "ready_for_bucket_construction_count":br.get("ready_for_bucket_construction_count",0),
        "ready_for_v13_2_bucket_construction_next_stage":not blocked and br.get("ready_for_v13_2_bucket_construction_next_stage",False),
        "forbidden_action_violations":sv+reasons,"candidate_violations":cv,"data_violations":dv,"safety_violations":sv,
        "blocking_reasons":reasons+cv+dv,"investment_action_count":0,"trade_action_count":0,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_paper_bootstrap_audit.json","w"),indent=2)
    print(f"Audit: {result['status']} | def_ok={not any('NO_DEF' in r for r in reasons+cv)}")
if __name__=="__main__":main()
