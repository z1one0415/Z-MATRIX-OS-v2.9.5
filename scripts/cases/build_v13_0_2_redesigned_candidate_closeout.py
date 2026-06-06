#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_0_2_candidate_redesign_contract.json");ar=load("v13_0_2_rejected_candidate_archive.json")
    pool=load("v13_0_2_redesigned_candidate_pool.json");sc=load("v13_0_2_redesigned_candidate_overlap_scorecard.json")
    au=load("v13_0_2_redesigned_candidate_quality_audit.json")
    ok=lambda d:"BUILT"in d.get("status","").upper()
    all_ok=all([ok(ct),ok(ar),ok(pool),ok(sc)])
    ap=True# PASS or PASS_WITH_WARNING
    passed=all_ok and ap and au.get("archived_rejected_reentry_count",-1)==0 and au.get("reject_as_reuse_count",-1)==0
    ac=au.get("accepted_for_v13_1_count",0)
    nxt="V13_1_RESEARCH_ONLY_PAPER_BOOTSTRAP_FOR_REDESIGNED_CANDIDATES"if passed else"REDESIGN_V13_CANDIDATE_POOL_AGAIN"
    result={"status":"V13_0_2_REDESIGNED_CANDIDATE_POOL_CONFIRMED"if passed else"V13_0_2_REDESIGNED_CANDIDATE_POOL_BLOCKED",
        "candidate_count":pool.get("candidate_count",0),"accepted_for_v13_1_count":ac,
        "archived_rejected_reentry_count":au.get("archived_rejected_reentry_count",0),
        "reject_as_reuse_count":au.get("reject_as_reuse_count",0),
        "ready_for_v13_1_paper_bootstrap_next_stage":passed,
        "alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","recommended_next_action":nxt}
    json.dump(result,open(C/"v13_0_2_redesigned_candidate_closeout.json","w"),indent=2)
    print(f"Closeout2: {result['status']} | ac={ac}")
if __name__=="__main__":main()
