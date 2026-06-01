#!/usr/bin/env python3
"""V10-F: Build V10 closeout — validates upstream status (not hardcoded)."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"

def main():
    inp=json.loads((C/"v10_council_input_pack.json").read_text())
    cr=json.loads((C/"v10_research_council_review.json").read_text())
    da=json.loads((C/"v10_devil_advocate_review.json").read_text())
    tp=json.loads((C/"v10_candidate_factor_thesis_pack.json").read_text())
    v11=json.loads((C/"v11_paper_watchlist_entry_gate.json").read_text())
    co={"status":"CASE_EXPANSION_V10_COUNCIL_RESEARCH_REVIEW_CONFIRMED" if v11["ready_for_paper_watchlist"] else "CASE_EXPANSION_V10_BLOCKED","council_input_pack_built":inp["status"]=="V10_COUNCIL_INPUT_PACK_BUILT","research_council_review_built":cr["status"]=="V10_RESEARCH_COUNCIL_REVIEW_BUILT","devil_advocate_review_built":da["status"]=="V10_DEVIL_ADVOCATE_REVIEW_BUILT","candidate_factor_thesis_pack_built":tp["status"]=="V10_CANDIDATE_FACTOR_THESIS_PACK_BUILT","v11_paper_watchlist_entry_gate_built":True,"reviewed_factor_count":len(cr["reviews"]),"candidate_count":tp["candidate_count"],"evidence_missing_count":tp["evidence_missing_count"],"critical_blockers":da["critical_blockers"],"ready_for_paper_watchlist":v11["ready_for_paper_watchlist"],"ready_for_alpha_claim":False,"alpha_validated":False,"investment_action_count":0,"buy_sell_instruction_count":0,"council_investment_verdict":"BLOCKED_RESEARCH_REVIEW_ONLY","production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(co,open(C/"case_expansion_v10_closeout.json","w"),indent=2)
    print(f"Closeout: {co['status']}")

if __name__=="__main__": main()
