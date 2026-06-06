#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    co=load("v13_0_1_candidate_overlap_closeout.json");sc=load("v13_0_1_candidate_overlap_scorecard.json")
    ok="REDESIGN"in co.get("recommended_next_action","")
    ct={"status":"V13_0_2_CANDIDATE_REDESIGN_CONTRACT_BUILT"if ok else"V13_0_2_CANDIDATE_REDESIGN_CONTRACT_BLOCKED",
        "redesign_mode":"REPLACE_REJECTED_HIGH_OVERLAP_CANDIDATES","preserve_accepted_candidate_count":sc.get("pass_overlap_count",3),
        "rejected_candidate_count":sc.get("reject_as_reuse_count",5),"target_candidate_count":8,
        "min_accepted_for_v13_1":4,"preferred_accepted_for_v13_1":6,"requires_overlap_rescoring":True,
        "requires_universe_gate":True,"ready_for_v13_1_paper_bootstrap":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(ct,open(C/"v13_0_2_candidate_redesign_contract.json","w"),indent=2)
    print(f"Contract: {ct['status']}")
if __name__=="__main__":main()
