#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_0_research_restart_contract.json");freeze=load("v13_0_v12_failure_freeze_manifest.json")
    dl=load("v13_0_failed_seed_denylist.json");autopsy=load("v13_0_v12_failure_autopsy_summary.json")
    ug=load("v13_0_universe_eligibility_gate_contract.json");us=load("v13_0_universe_eligibility_scan.json")
    dc=load("v13_0_candidate_discovery_contract.json");pool=load("v13_0_new_candidate_pool.json")
    au=load("v13_0_candidate_quality_gate_audit.json")
    ok=lambda d:"BUILT"in d.get("status","").upper()
    all_ok=all([ok(ct),ok(freeze),ok(dl),ok(autopsy),ok(ug),ok(us),ok(dc),ok(pool)])
    ap="PASS"in au.get("status","")
    sf=all([ct.get("production")=="BLOCKED",ct.get("broker_runtime")=="BLOCKED",ct.get("real_trade")=="BLOCKED"])
    passed=all_ok and ap and sf
    nxt=au.get("ready_for_v13_1_paper_bootstrap_next_stage",False)
    act="V13_1_RESEARCH_ONLY_PAPER_BOOTSTRAP_FOR_NEW_CANDIDATES"if nxt else"FIX_V13_0_CANDIDATE_DISCOVERY"
    result={"status":"V13_0_RESEARCH_RESTART_CONFIRMED"if passed else"V13_0_RESEARCH_RESTART_BLOCKED",
        "v12_loop_closed":True,"v12_failed_seed_denied":True,"universe_gate_confirmed":us.get("universe_scan_ready_for_candidate_generation",False),
        "accepted_candidate_count":pool.get("accepted_candidate_count",0),
        "blocked_candidate_count":pool.get("blocked_candidate_count",0),
        "rejected_candidate_count":pool.get("rejected_candidate_count",0),
        "ready_for_v13_1_paper_bootstrap_next_stage":nxt,"alpha_claim_allowed":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","recommended_next_action":act}
    json.dump(result,open(C/"v13_0_research_restart_closeout.json","w"),indent=2)
    print(f"Closeout: {result['status']} | ac={result['accepted_candidate_count']} nxt={nxt}")
if __name__=="__main__":main()
