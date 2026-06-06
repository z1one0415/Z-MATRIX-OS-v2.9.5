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
    ct=load("v13_0_candidate_discovery_contract.json");pool=load("v13_0_new_candidate_pool.json")
    dl=load("v13_0_failed_seed_denylist.json");us=load("v13_0_universe_eligibility_scan.json")
    reasons=[];cv=[];sv=[]
    targets=[("contract",ct),("pool",pool),("denylist",dl),("universe",us)]
    for fn,d in targets:
        if d.get("ready_for_alpha_claim",False):reasons.append(f"ALPHA_{fn}")
        if d.get("alpha_validated",False):reasons.append(f"AV_{fn}")
    min_cand=ct.get("candidate_count_min",4)
    if pool.get("accepted_candidate_count",0)<min_cand:reasons.append(f"TOO_FEW_CANDIDATES={pool.get('accepted_candidate_count')}")
    if pool.get("failed_seed_reuse_violation_count",0)!=0:cv.append(f"REUSE_VIOLATION={pool.get('failed_seed_reuse_violation_count')}")
    for c in pool.get("candidates",[]):
        if not c.get("denied_by_denylist"):
            if not c.get("hypothesis_id"):cv.append(f"NO_HYP:{c.get('candidate_id')}")
            if not c.get("factor_definition_hash"):cv.append(f"NO_HASH:{c.get('candidate_id')}")
            if c.get("failed_seed_overlap_score",0)>=0.75:cv.append(f"OVERLAP:{c.get('candidate_id')}")
    for fn,d in targets:sv.extend(scan(d,fn))
    blocked=len(reasons)+len(cv)+len(sv)>0
    result={"status":"V13_0_CANDIDATE_QUALITY_GATE_AUDIT_PASS"if not blocked else"V13_0_CANDIDATE_QUALITY_GATE_AUDIT_BLOCKED",
        "candidate_quality_gate_confirmed":not blocked,"accepted_candidate_count":pool.get("accepted_candidate_count",0),
        "failed_seed_reuse_violation_count":0,"ready_for_v13_1_paper_bootstrap_next_stage":not blocked,
        "forbidden_action_violations":sv+reasons,"candidate_violations":cv,"safety_violations":sv,
        "blocking_reasons":reasons+cv,"investment_action_count":0,"trade_action_count":0,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_candidate_quality_gate_audit.json","w"),indent=2)
    print(f"QualityGate: {result['status']} | ac={result['accepted_candidate_count']}")
if __name__=="__main__":main()
