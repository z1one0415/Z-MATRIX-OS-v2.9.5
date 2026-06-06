#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    pool=load("v13_0_new_candidate_pool.json");sc=load("v13_0_1_candidate_overlap_scorecard.json")
    sc_map={s["candidate_id"]:s for s in sc.get("scorecards",[])}
    archived=[]
    for c in pool.get("candidates",[]):
        s=sc_map.get(c["candidate_id"],{})
        if s.get("overlap_decision")=="REJECT_AS_FAILED_SEED_REUSE":
            archived.append({"candidate_id":c["candidate_id"],"factor_name":c["factor_name"],
                "failed_tokens_used":s.get("failed_tokens_used",[]),"computed_overlap_score":s.get("computed_overlap_score"),
                "rejection_reason":"FAILED_SEED_REUSE_OVERLAP_TOO_HIGH","reuse_allowed_in_v13_0_2":False})
    result={"status":"V13_0_2_REJECTED_CANDIDATE_ARCHIVE_BUILT","rejected_count":len(archived),
        "rejected_candidates":archived,"ready_for_redesigned_pool":True,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_2_rejected_candidate_archive.json","w"),indent=2)
    print(f"Archive: {len(archived)} rejected archived")
if __name__=="__main__":main()
