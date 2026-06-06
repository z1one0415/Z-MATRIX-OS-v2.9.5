#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    freeze=load("v13_0_v12_failure_freeze_manifest.json")
    items=[]
    for ff in freeze.get("frozen_factors",[]):
        items.append({"factor_id":ff["factor_id"],"horizon":ff["horizon"],"final_state":ff["final_state"],
            "policy_decision":"DO_NOT_PROMOTE","reuse_allowed":False,"reuse_exception_allowed":True,
            "reuse_exception_condition":"MUST_BE_REDESIGNED_WITH_NEW_DEFINITION_AND_NEW_HYPOTHESIS"})
    result={"status":"V13_0_FAILED_SEED_DENYLIST_BUILT","denylist_policy":"BLOCK_FAILED_V12_SEED_REUSE",
        "denylist_count":len(items),"denylist_items":items,"direct_reuse_allowed_count":0,
        "ready_for_candidate_filtering":True,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_failed_seed_denylist.json","w"),indent=2)
    print(f"Denylist: {len(items)} factors denied")
if __name__=="__main__":main()
