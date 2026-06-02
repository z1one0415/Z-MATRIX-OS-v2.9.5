#!/usr/bin/env python3
"""V11.5 Entry Gate."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
co=json.loads((C/"case_expansion_v11_closeout.json").read_text())
ok=co.get("status")=="CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED"
g={"status":"V11_5_PAPER_PORTFOLIO_SIMULATION_ENTRY_ALLOWED" if ok else"BLOCKED","ready_for_paper_portfolio_simulation":ok,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(g,open(C/"v11_5_paper_portfolio_entry_gate.json","w"),indent=2)
print(f"V11.5: {'ALLOWED' if ok else 'BLOCKED'}")
