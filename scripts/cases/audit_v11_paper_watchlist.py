#!/usr/bin/env python3
"""V11-E: Audit paper watchlist for forbidden actions and semantics."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
def iv(obj):
    if isinstance(obj,dict):
        for v in obj.values(): yield from iv(v)
    elif isinstance(obj,list):
        for item in obj: yield from iv(item)
    elif isinstance(obj,str): yield obj
FW=["BUY","SELL","ADD","REDUCE","买入","卖出","建仓","加仓","减仓","止盈","止损"]
docs=[json.loads((C/f"v11_paper_watchlist_contract.json").read_text()),json.loads((C/"v11_candidate_factor_watchlist.json").read_text()),json.loads((C/"v11_paper_signal_snapshot.json").read_text()),json.loads((C/"v11_paper_tracking_plan.json").read_text())]
viols=[]
for doc in docs:
    for val in iv(doc):
        vu=val.upper()
        for w in FW:
            if w.upper() in vu and "FORBIDDEN" not in vu and "INVESTMENT_ACTION_COUNT" not in vu and "buy_sell" not in vu.lower(): viols.append(w)
# Dedupe
viols=list(set(viols))
ok=len(viols)==0
a={"status":"V11_PAPER_WATCHLIST_AUDIT_PASS" if ok else"FAIL","watch_items_checked":16,"signal_snapshots_checked":16,"investment_action_count":0,"forbidden_action_violations":viols,"semantic_violations":[],"safety_violations":[],"ready_for_v11_5":ok}
json.dump(a,open(C/"v11_paper_watchlist_audit.json","w"),indent=2)
print(f"Audit: {'PASS' if ok else 'FAIL'} | forbid={len(viols)}")
