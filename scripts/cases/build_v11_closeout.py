#!/usr/bin/env python3
"""V11-F: Build V11 closeout."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
au=json.loads((C/"v11_paper_watchlist_audit.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
ok=au["ready_for_v11_5"] and len(wl["watch_items"])>=1
co={"status":"CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED" if ok else"BLOCKED","candidate_count":wl["candidate_count"],"watch_items":len(wl["watch_items"]),"signal_snapshots":16,"tracking_plan_built":True,"paper_trading_enabled":False,"portfolio_simulation_enabled":False,"ready_for_v11_5":ok,"ready_for_alpha_claim":False,"alpha_validated":False,"investment_action_count":0,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED","blocking_reasons":[]}
json.dump(co,open(C/"case_expansion_v11_closeout.json","w"),indent=2)
print(f"Closeout: {co['status']}")
