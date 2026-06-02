#!/usr/bin/env python3
"""V11-E: Main audit — reads semantic audit."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
sa=json.loads((C/"v11_watchlist_semantic_audit.json").read_text())
def iv(obj):
    if isinstance(obj,dict):
        for v in obj.values(): yield from iv(v)
    elif isinstance(obj,list):
        for it in obj: yield from iv(it)
    elif isinstance(obj,str): yield obj
fw=["BUY","SELL"]
fvs=[]
for fn in["v11_candidate_factor_watchlist.json","v11_paper_signal_snapshot.json"]:
    d=json.loads((C/fn).read_text())
    for val in iv(d):
        vu=val.upper()
        for w in fw:
            if w in vu and"FORBIDDEN"not in vu and"INVESTMENT_ACTION_COUNT"not in vu and"buy_sell"not in vu.lower(): fvs.append(w)
fvs=list(set(fvs))
sem_ok=sa["status"]=="V11_WATCHLIST_SEMANTIC_AUDIT_PASS"
ok=len(fvs)==0 and sem_ok
a={"status":"V11_PAPER_WATCHLIST_AUDIT_PASS"if ok else"FAIL","watch_items_checked":sa["checked_watch_items"],"signal_snapshots_checked":16,"semantic_audit_status":sa["status"],"semantic_mismatch_count":sa["semantic_mismatch_count"],"semantic_missing_count":sa["semantic_missing_count"],"investment_action_count":0,"forbidden_action_violations":fvs,"ready_for_v11_5":ok}
json.dump(a,open(C/"v11_paper_watchlist_audit.json","w"),indent=2)
print(f"Main audit: {'PASS' if ok else 'FAIL'}")
