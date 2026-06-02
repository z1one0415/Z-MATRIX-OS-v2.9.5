#!/usr/bin/env python3
"""V11-B: Build candidate factor watchlist from V10 thesis."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
tp=json.loads((C/"v10_candidate_factor_thesis_pack.json").read_text())
items=[];a=l=r=0
for i,c in enumerate(tp["candidates"],1):
    ev=c["supporting_evidence"];rd=ev.get("rankic_direction","MIXED");rg=ev.get("robustness_grade","REVIEW")
    if rd=="MIXED" or rg not in ("ROBUST","REVIEW"): st="WATCH_WITH_LIMITATION";l+=1
    elif any(ev.get(k) is None for k in["mean_rankic","rankic_ir"]): st="REJECT_FROM_WATCHLIST";r+=1
    else: st="ACTIVE_PAPER_WATCH";a+=1
    bu="LOW_FACTOR_VALUE_FAVORED" if rd=="NEGATIVE" else("HIGH_FACTOR_VALUE_FAVORED" if rd=="POSITIVE" else"NO_PREFERRED_DIRECTION")
    items.append({"watch_id":f"V11_WATCH_{i:03d}","factor_id":c["factor_id"],"horizon":c["horizon"],"rankic_direction":rd,"decay_pattern":ev.get("decay_pattern"),"decay_pattern_basis":ev.get("decay_pattern_basis"),"raw_rankic_trend":ev.get("raw_rankic_trend"),"robustness_grade":rg,"bucket_direction":bu,"paper_tracking_required":True,"watch_status":st,"investment_action":"NONE","ready_for_alpha_claim":False,"alpha_validated":False})
wl={"status":"V11_CANDIDATE_FACTOR_WATCHLIST_BUILT","candidate_count":tp["candidate_count"],"watch_items":len(items),"active_paper_watch":a,"watch_with_limitation":l,"rejected_from_watchlist":r,"watch_items":items,"investment_action_count":0,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(wl,open(C/"v11_candidate_factor_watchlist.json","w"),indent=2)
print(f"Watchlist: {a}A/{l}L/{r}R")
