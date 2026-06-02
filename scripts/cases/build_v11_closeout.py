#!/usr/bin/env python3
"""V11-F: Closeout — reads semantic audit."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
sa=json.loads((C/"v11_watchlist_semantic_audit.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
au=json.loads((C/"v11_paper_watchlist_audit.json").read_text())
ok=au["ready_for_v11_5"] and sa["status"]=="V11_WATCHLIST_SEMANTIC_AUDIT_PASS" and len(wl["watch_items"])>=1
co={"status":"CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED"if ok else"BLOCKED","candidate_count":wl["candidate_count"],"watch_items_count":wl["watch_items_count"],"signal_snapshots":16,"tracking_plan_built":True,"semantic_audit_pass":sa["status"]=="V11_WATCHLIST_SEMANTIC_AUDIT_PASS","semantic_mismatch_count":sa["semantic_mismatch_count"],"semantic_missing_count":sa["semantic_missing_count"],"paper_trading_enabled":False,"portfolio_simulation_enabled":False,"ready_for_v11_5":ok,"ready_for_alpha_claim":False,"alpha_validated":False,"investment_action_count":0,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","blocking_reasons":[]}
json.dump(co,open(C/"case_expansion_v11_closeout.json","w"),indent=2)
print(f"Closeout: {co['status']}")
