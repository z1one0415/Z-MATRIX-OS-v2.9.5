#!/usr/bin/env python3
"""V10-D: Build candidate factor thesis pack — evidence-complete only."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"

def main():
    cr=json.loads((C/"v10_research_council_review.json").read_text())
    cands=[]; em=0; ci=0
    for rv in cr["reviews"]:
        if rv["final_research_verdict"] in ("RESEARCH_APPROVED","WATCH_ONLY"):
            ev=rv["evidence"]
            required=["mean_rankic","rankic_ir","valid_date_count","decay_pattern","robustness_grade"]
            if any(ev.get(k) is None for k in required):
                em+=1; continue
            ci+=1; fid=rv["factor_id"]
            th=f"Factor {fid} shows meaningful signal at {rv['horizon']} horizon."
            cands.append({"candidate_id":f"V10_CAND_{ci:03d}","factor_id":fid,"horizon":rv["horizon"],"research_thesis":th,"supporting_evidence":ev,"counter_arguments":["May be size/liquidity proxy." if ("AMOUNT" in fid or "VOLUME" in fid) else "Signal may not persist.","No transaction cost model.","No fundamental cross-validation."],"paper_tracking_required":True,"ready_for_alpha_claim":False,"alpha_validated":False,"investment_action":"NONE"})
    tp={"status":"V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT","candidate_count":len(cands),"evidence_complete_count":len(cands),"evidence_missing_count":em,"investment_action_count":0,"candidates":cands,"ready_for_alpha_claim":False}
    json.dump(tp,open(C/"v10_candidate_factor_thesis_pack.json","w"),indent=2)
    print(f"Thesis: {len(cands)} candidates, {em} evidence_missing, 0 investments")

if __name__=="__main__": main()
