#!/usr/bin/env python3
import json,re;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
IW=["AND","ratio","adjusted","neutral","rank","gate","filter","interaction","compression","breakout","persistence","dry_up","DRAWDOWN","industry_neutral","regime","cross_section","dispersion","recovery","stability","acceleration","diff","shock","event_clean"]
NW=["sector","industry","drawdown","fundamental","downside","regime","rank_dynamics","recovery","turnover","stability","quality","event_clean","acceleration","dispersion","neutral"]
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def score(c,tokens,fh):
    d=c.get("factor_definition","").upper();n=c.get("factor_name","").upper()
    ut=[];raw=False;hr=False
    for t in tokens:
        if t.upper()in d:ut.append(t)
    tc=len(ut);tr=tc/len(tokens)if tokens else 0
    if any(t.upper()==n for t in tokens):raw=True
    elif tc>=3 and not any(w.upper()in d for w in IW):raw=True
    for h in fh:
        if h["factor_id"]in ut and h["horizon"]==c.get("target_horizon",""):hr=True
    intr=any(w.upper()in d for w in IW);ni=any(w.upper()in d for w in NW)
    if raw:s=1.0
    else:
        s=min(1.0,tc/3)
        if hr:s+=0.10
        if tc>=3:s+=0.20
        if not ni and tc>=2:s+=0.25
        if intr:s-=0.10
        if ni:s-=0.20
        if c.get("factor_definition_hash"):s-=0.05
    s=max(0.0,min(1.0,round(s,3)))
    if s>=0.75:dec="REJECT_AS_FAILED_SEED_REUSE"
    elif s>=0.45:dec="REQUIRE_REDESIGN_JUSTIFICATION"
    else:dec="PASS_OVERLAP_GATE"
    # Extra gate: new candidates must have new_info
    if c.get("is_new_candidate")and not ni:dec="REQUIRE_REDESIGN_JUSTIFICATION";s=max(s,0.45)
    if c.get("is_new_candidate")and tc>1:dec="REQUIRE_REDESIGN_JUSTIFICATION";s=max(s,0.45)
    return {"candidate_id":c.get("candidate_id"),"factor_name":c.get("factor_name"),
        "target_horizon":c.get("target_horizon"),"failed_tokens_used":ut,"token_overlap_count":tc,
        "token_overlap_ratio":round(tr,3),"horizon_reuse_flag":hr,"raw_reuse_flag":raw,
        "interaction_claim_flag":intr,"new_information_source_flag":ni,"computed_overlap_score":s,
        "overlap_decision":dec,"blocking_reasons":[]if dec=="PASS_OVERLAP_GATE"else[dec]}
def main():
    pool=load("v13_0_2_redesigned_candidate_pool.json");idx=load("v13_0_1_failed_seed_token_index.json")
    tokens=idx.get("failed_factor_tokens",[]);fh=idx.get("failed_horizon_pairs",[])
    items=[];pa=0;rr=0;rj=0
    for c in pool.get("candidates",[]):
        r=score(c,tokens,fh);items.append(r)
        if r["overlap_decision"]=="PASS_OVERLAP_GATE":pa+=1
        elif r["overlap_decision"]=="REQUIRE_REDESIGN_JUSTIFICATION":rr+=1
        else:rj+=1
    mx=max((i["computed_overlap_score"]for i in items),default=0)
    result={"status":"V13_0_2_REDESIGNED_CANDIDATE_OVERLAP_SCORECARD_BUILT","candidate_count":len(items),
        "pass_overlap_count":pa,"require_redesign_justification_count":rr,"reject_as_reuse_count":rj,
        "max_overlap_score":mx,"scorecards":items,"ready_for_redesign_quality_gate":True,
        "ready_for_v13_1_paper_bootstrap":False,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_2_redesigned_candidate_overlap_scorecard.json","w"),indent=2)
    print(f"Overlap2: pa={pa} rr={rr} rj={rj} max={mx}")
if __name__=="__main__":main()
