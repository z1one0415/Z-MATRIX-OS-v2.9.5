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
            if any(ev.get(k) is None for k in ["mean_rankic","rankic_ir","valid_date_count","decay_pattern","robustness_grade"]): em+=1; continue
            ci+=1; fid=rv["factor_id"]
            cands.append(dict(candidate_id=f"V10_CAND_{ci:03d}",factor_id=fid,horizon=rv["horizon"],research_thesis=f"Factor {fid} shows meaningful signal at {rv["horizon"]}.",supporting_evidence=ev,counter_arguments=["May be proxy.","No cost model."],paper_tracking_required=True,ready_for_alpha_claim=False,alpha_validated=False,investment_action="NONE"))
    tp=dict(status="V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT",candidate_count=len(cands),evidence_complete_count=len(cands),evidence_missing_count=em,investment_action_count=0,candidates=cands,ready_for_alpha_claim=False,alpha_validated=False,production="BLOCKED",broker_runtime="BLOCKED",real_trade="BLOCKED")
    json.dump(tp,open(C/"v10_candidate_factor_thesis_pack.json","w"),indent=2)
    print(f"Thesis: {len(cands)} candidates, {em} missing")
if __name__=="__main__": main()
