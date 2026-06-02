#!/usr/bin/env python3
"""V11.5 Entry Gate — reads semantic audit."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
sa=json.loads((C/"v11_watchlist_semantic_audit.json").read_text())
au=json.loads((C/"v11_paper_watchlist_audit.json").read_text())
co=json.loads((C/"case_expansion_v11_closeout.json").read_text())
ok=(sa["status"]=="V11_WATCHLIST_SEMANTIC_AUDIT_PASS" and au["ready_for_v11_5"] and co.get("status")=="CASE_EXPANSION_V11_PAPER_WATCHLIST_CONFIRMED" and sa["semantic_mismatch_count"]==0 and sa["semantic_missing_count"]==0)
g={"status":"V11_5_PAPER_PORTFOLIO_SIMULATION_ENTRY_ALLOWED"if ok else"BLOCKED","ready_for_paper_portfolio_simulation":ok,"semantic_audit_pass":sa["status"]=="V11_WATCHLIST_SEMANTIC_AUDIT_PASS","ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(g,open(C/"v11_5_paper_portfolio_entry_gate.json","w"),indent=2)
print(f"V11.5: {'ALLOWED' if ok else 'BLOCKED'}")
