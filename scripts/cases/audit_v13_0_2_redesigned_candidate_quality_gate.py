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
    pool=load("v13_0_2_redesigned_candidate_pool.json");ar=load("v13_0_2_rejected_candidate_archive.json")
    sc=load("v13_0_2_redesigned_candidate_overlap_scorecard.json");us=load("v13_0_universe_eligibility_scan.json")
    reasons=[];cv=[];sv=[]
    targets=[("pool",pool),("scorecard",sc),("archive",ar)]
    for fn,d in targets:
        if d.get("ready_for_alpha_claim",False):reasons.append(f"ALPHA_{fn}")
        if d.get("alpha_validated",False):reasons.append(f"AV_{fn}")
    # Archived must not re-enter
    arch_ids=set(c["candidate_id"]for c in ar.get("rejected_candidates",[]))
    pool_ids=set(c["candidate_id"]for c in pool.get("candidates",[]))
    reentry=arch_ids&pool_ids
    if reentry:cv.append(f"ARCHIVED_REJECTED_REENTRY:{reentry}")
    rej=sc.get("reject_as_reuse_count",0)
    if rej>0:cv.append(f"REJECT={rej}")
    pa=sc.get("pass_overlap_count",0);rr=sc.get("require_redesign_justification_count",0)
    ac=pa# Only PASS count
    pref=ac>=6
    if ac<4:reasons.append(f"TOO_FEW_ACCEPTED={ac}")
    for c in pool.get("candidates",[]):
        if c.get("is_new_candidate"):
            if not c.get("hypothesis_id"):cv.append(f"NO_HYP:{c.get('candidate_id')}")
            if not c.get("factor_definition_hash"):cv.append(f"NO_HASH:{c.get('candidate_id')}")
    for fn,d in targets:sv.extend(scan(d,fn))
    blocked=len(reasons)+len(cv)+len(sv)>0 or rej>0
    st="V13_0_2_REDESIGNED_CANDIDATE_QUALITY_AUDIT_PASS"if not blocked else"V13_0_2_REDESIGNED_CANDIDATE_QUALITY_AUDIT_BLOCKED"
    if not blocked and not pref:st+="_WITH_WARNING"
    result={"status":st,"accepted_for_v13_1_count":ac,"preferred_target_met":pref,
        "archived_rejected_reentry_count":len(reentry),"reject_as_reuse_count":rej,
        "ready_for_v13_1_paper_bootstrap_next_stage":not blocked,
        "forbidden_action_violations":sv+reasons,"candidate_violations":cv,"safety_violations":sv,
        "blocking_reasons":reasons+cv,"investment_action_count":0,"trade_action_count":0,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_2_redesigned_candidate_quality_audit.json","w"),indent=2)
    print(f"QGate2: {result['status']} | ac={ac} pref={pref}")
if __name__=="__main__":main()
