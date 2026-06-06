#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_1_paper_bootstrap_contract.json");reg=load("v13_1_candidate_registry.json")
    fa=load("v13_1_candidate_field_availability.json");lc=load("v13_1_label_coverage.json")
    br=load("v13_1_bucket_readiness.json");au=load("v13_1_paper_bootstrap_audit.json")
    ok=lambda d:"BUILT"in d.get("status","").upper()
    all_ok=all([ok(ct),ok(reg),ok(fa),ok(lc),ok(br)])
    ap="PASS"in au.get("status","")
    passed=all_ok and ap
    ready=br.get("ready_for_v13_2_bucket_construction_next_stage",False)
    nxt="V13_2_RESEARCH_ONLY_BUCKET_CONSTRUCTION"if ready else"FIX_V13_1_FIELD_AVAILABILITY_OR_REDESIGN_CANDIDATES"
    result={"status":"V13_1_PAPER_BOOTSTRAP_CONFIRMED"if passed else"V13_1_PAPER_BOOTSTRAP_BLOCKED",
        "registered_candidate_count":reg.get("registered_candidate_count",8),
        "ready_for_bucket_construction_count":br.get("ready_for_bucket_construction_count",0),
        "blocked_candidate_count":br.get("blocked_candidate_count",0),
        "ready_for_v13_2_bucket_construction_next_stage":ready,
        "alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","recommended_next_action":nxt}
    json.dump(result,open(C/"v13_1_paper_bootstrap_closeout.json","w"),indent=2)
    print(f"Closeout: {result['status']} | ready={ready}")
if __name__=="__main__":main()
