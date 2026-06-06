#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    pool=load("v13_0_2_redesigned_candidate_pool.json");sc=load("v13_0_2_redesigned_candidate_overlap_scorecard.json")
    sc_map={s["candidate_id"]:s for s in sc.get("scorecards",[])}
    items=[];exc=[]
    for c in pool.get("candidates",[]):
        s=sc_map.get(c["candidate_id"],{})
        if s.get("overlap_decision")=="PASS_OVERLAP_GATE":
            items.append({"v13_1_candidate_run_id":f"V13_1_RUN_{len(items)+1:03d}","candidate_id":c["candidate_id"],
                "hypothesis_id":c.get("hypothesis_id",""),"candidate_family":c.get("candidate_family",""),
                "factor_name":c["factor_name"],"factor_definition":c.get("factor_definition",""),
                "factor_definition_hash":c.get("factor_definition_hash",""),"target_horizon":c["target_horizon"],
                "expected_direction":c.get("expected_direction","POSITIVE"),"overlap_decision":"PASS_OVERLAP_GATE",
                "is_new_candidate":c.get("is_new_candidate",False),"eligible_universe_only":True,
                "universe_gate_required":True,"paper_only":True,"investment_action":"NONE","trade_action":"NONE"})
        elif s.get("overlap_decision"):
            exc.append(c["factor_name"])
    result={"status":"V13_1_CANDIDATE_REGISTRY_BUILT","registered_candidate_count":len(items),
        "excluded_candidate_count":len(exc),"excluded_candidates":exc,
        "registry_items":items,"registry_ready_for_bucket_readiness":True,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_candidate_registry.json","w"),indent=2)
    print(f"Registry: {len(items)} registered, {len(exc)} excluded")
if __name__=="__main__":main()
