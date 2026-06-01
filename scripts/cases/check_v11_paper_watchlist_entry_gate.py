#!/usr/bin/env python3
"""V10-E: V11 paper watchlist entry gate — hardened with full checks."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"

def main():
    cr=json.loads((C/"v10_research_council_review.json").read_text())
    da=json.loads((C/"v10_devil_advocate_review.json").read_text())
    tp=json.loads((C/"v10_candidate_factor_thesis_pack.json").read_text())
    bl=[]
    if cr.get("status")!="V10_RESEARCH_COUNCIL_REVIEW_BUILT": bl.append("COUNCIL_REVIEW_NOT_BUILT")
    if da.get("status")!="V10_DEVIL_ADVOCATE_REVIEW_BUILT": bl.append("DEVIL_ADVOCATE_NOT_BUILT")
    if tp.get("status")!="V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT": bl.append("THESIS_PACK_NOT_BUILT")
    if tp.get("candidate_count",0)<1: bl.append("NO_CANDIDATES")
    if tp.get("evidence_missing_count",0)>0: bl.append("EVIDENCE_MISSING")
    if da.get("critical_blockers",0)>0: bl.append("CRITICAL_BLOCKERS_PRESENT")
    if tp.get("investment_action_count",0)>0: bl.append("INVESTMENT_ACTION_DETECTED")
    if tp.get("ready_for_alpha_claim",False) or cr.get("ready_for_alpha_claim",False): bl.append("ALPHA_CLAIM_DETECTED")
    ok=len(bl)==0
    g={"status":"V11_PAPER_WATCHLIST_ENTRY_ALLOWED" if ok else "V11_ENTRY_BLOCKED","ready_for_paper_watchlist":ok,"candidate_count":tp["candidate_count"],"evidence_missing_count":tp["evidence_missing_count"],"critical_blockers":da["critical_blockers"],"investment_action_count":tp["investment_action_count"],"ready_for_alpha_claim":False,"alpha_validated":False,"blocking_reasons":bl,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(g,open(C/"v11_paper_watchlist_entry_gate.json","w"),indent=2)
    print(f"V11: {'ALLOWED' if ok else 'BLOCKED'} | reasons={bl}")

if __name__=="__main__": main()
