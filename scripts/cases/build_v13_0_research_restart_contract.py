#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    co=load("v12_5_multicycle_feedback_closeout.json");fc=load("v12_5_multicycle_feedback_full_chain.json")
    sd=load("v12_5_next_seed_discipline_update.json")
    ok="CONFIRMED"in co.get("status","")and sd.get("next_cycle_seed_count",-1)==0
    ct={"status":"V13_0_RESEARCH_RESTART_CONTRACT_BUILT"if ok else"V13_0_RESEARCH_RESTART_CONTRACT_BLOCKED",
        "restart_mode":"NEW_CANDIDATE_DISCOVERY_AFTER_FAILED_RESEARCH_LOOP",
        "v12_cycle_count":2,"v12_total_hit_count":0,"v12_total_observation_count":12,
        "v12_alpha_claim_allowed":False,"v12_next_cycle_seed_count":0,"v12_research_loop_closed":True,
        "v13_must_not_reuse_failed_seed":True,"v13_requires_universe_eligibility_gate":True,
        "v13_requires_suspension_filter":True,"v13_requires_full_label_coverage":True,
        "v13_candidate_discovery_allowed":True,"v13_paper_bootstrap_allowed":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(ct,open(C/"v13_0_research_restart_contract.json","w"),indent=2)
    print(f"Contract: {ct['status']}")
if __name__=="__main__":main()
