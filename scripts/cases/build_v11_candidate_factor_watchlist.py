#!/usr/bin/env python3
"""V11-B: Build candidate factor watchlist with semantic completeness check."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
tp=json.loads((C/"v10_candidate_factor_thesis_pack.json").read_text())
items=[]; sem_miss=[]; a=l=r=0
for i,c in enumerate(tp["candidates"],1):
    fid=c["factor_id"];h=c["horizon"];ev=c["supporting_evidence"]
    rd=ev.get("rankic_direction","MISSING");dp=ev.get("decay_pattern","MISSING")
    db=ev.get("decay_pattern_basis","MISSING");rt=ev.get("raw_rankic_trend","MISSING")
    rg=ev.get("robustness_grade","REVIEW")
    miss=[k for k,v in[("rankic_direction",rd),("decay_pattern_basis",db),("raw_rankic_trend",rt),("decay_pattern",dp)]if v is None or v=="MISSING"]
    sem_miss.extend(f"{fid}.{m}" for m in miss if miss)
    if miss: st="REJECT_FROM_WATCHLIST";r+=1;bu="NO_PREFERRED_DIRECTION"
    elif rd=="MIXED": st="WATCH_WITH_LIMITATION";l+=1;bu="NO_PREFERRED_DIRECTION"
    elif rd in("NEGATIVE","POSITIVE")and rg in("ROBUST","REVIEW"): st="ACTIVE_PAPER_WATCH";a+=1;bu="LOW_FACTOR_VALUE_FAVORED"if rd=="NEGATIVE"else"HIGH_FACTOR_VALUE_FAVORED"
    else: st="WATCH_WITH_LIMITATION";l+=1;bu="NO_PREFERRED_DIRECTION"
    items.append({"watch_id":f"V11_WATCH_{i:03d}","factor_id":fid,"horizon":h,"rankic_direction":rd,"decay_pattern":dp,"decay_pattern_basis":db,"raw_rankic_trend":rt,"robustness_grade":rg,"bucket_direction":bu,"paper_tracking_required":True,"watch_status":st,"investment_action":"NONE","ready_for_alpha_claim":False,"alpha_validated":False})
wl={"status":"V11_CANDIDATE_FACTOR_WATCHLIST_BUILT","candidate_count":tp["candidate_count"],"watch_items_count":len(items),"active_paper_watch":a,"watch_with_limitation":l,"rejected_from_watchlist":r,"semantic_missing_fields":sem_miss,"watch_items":items,"investment_action_count":0,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(wl,open(C/"v11_candidate_factor_watchlist.json","w"),indent=2)
print(f"Watchlist: {a}A/{l}L/{r}R | sem_miss={len(sem_miss)}")
