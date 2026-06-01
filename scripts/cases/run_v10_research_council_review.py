#!/usr/bin/env python3
"""V10-B: Multi-seat research council review with deterministic voting."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
def main():
    inp=json.loads((C/"v10_council_input_pack.json").read_text())
    revs=[]; a=0; w=0; x=0
    for pf in inp["promoted_factors"]:
        fid,mr,ir,vdc=pf["factor_id"],pf["mean_rankic"],pf["rankic_ir"],pf.get("valid_date_count",0)
        dp,dc,rg=pf.get("decay_pattern"),pf.get("decay_consistent",False),pf.get("robustness_grade")
        fs="RESEARCH_APPROVED" if mr and abs(mr)>=0.05 and vdc>=500 else("WATCH_ONLY" if mr and abs(mr)>=0.03 and vdc>=250 else"REJECT_FOR_NOW")
        mm="WATCH_ONLY" if("AMOUNT"in fid or"VOLUME"in fid)else"RESEARCH_APPROVED"
        rk="WATCH_ONLY" if ir is not None else"REJECT_FOR_NOW"
        fu="WATCH_ONLY"; ra="RESEARCH_APPROVED" if rg=="ROBUST" else("WATCH_ONLY" if rg=="REVIEW" else"REJECT_FOR_NOW")
        of="REJECT_FOR_NOW" if dp=="NO_CLEAR_PATTERN" else"WATCH_ONLY"
        hp="WATCH_ONLY" if mr and abs(mr)>=0.03 else"REJECT_FOR_NOW"
        votes=dict(Factor_Statistician=fs,Market_Microstructure_Skeptic=mm,Risk_Manager=rk,Fundamental_Skeptic=fu,Regime_Analyst=ra,Overfitting_Auditor=of,Human_PM_Reviewer=hp)
        rc=sum(1 for v in votes.values()if v=="REJECT_FOR_NOW"); rs=sum(1 for v in votes.values()if v=="RESEARCH_APPROVED")
        vd="REJECT_FOR_NOW" if rc>=2 else("RESEARCH_APPROVED" if rs>=3 else"WATCH_ONLY")
        if vd=="RESEARCH_APPROVED": a+=1
        elif vd=="WATCH_ONLY": w+=1
        else: x+=1
        revs.append(dict(factor_id=fid,horizon=pf["horizon"],evidence=dict(mean_rankic=mr,rankic_ir=ir,valid_date_count=vdc,positive_rankic_ratio=pf.get("positive_rankic_ratio"),decay_pattern=dp,robustness_grade=rg),council_votes=votes,final_research_verdict=vd,reason="Signal exists",ready_for_paper_watchlist=vd!="REJECT_FOR_NOW",ready_for_alpha_claim=False,alpha_validated=False,investment_verdict="BLOCKED"))
    cr=dict(status="V10_RESEARCH_COUNCIL_REVIEW_BUILT",council_seats=7,reviewed_factor_count=len(revs),council_verdict_distribution=dict(RESEARCH_APPROVED=a,WATCH_ONLY=w,REJECT_FOR_NOW=x),reviews=revs,alpha_validated=False,ready_for_alpha_claim=False,production="BLOCKED",broker_runtime="BLOCKED",real_trade="BLOCKED")
    json.dump(cr,open(C/"v10_research_council_review.json","w"),indent=2)
    print(f"Council: {a}R/{w}W/{x}X")
if __name__=="__main__": main()
