#!/usr/bin/env python3
"""V12 Entry Gate — blocks partial and unconfirmed."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
co=json.loads((C/"case_expansion_v11_5_closeout.json").read_text())
reasons=["PAPER_TRACKING_PERIOD_NOT_COMPLETED","COST_MODEL_PROXY_ONLY","NO_OUT_OF_SAMPLE_LIVE_TRACKING"]
if co.get("status")=="CASE_EXPANSION_V11_5_BLOCKED_PARTIAL_RESULTS":reasons.insert(0,"V11_5_PARTIAL_RESULTS_ONLY")
elif co.get("status")!="CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED":reasons.insert(0,"V11_5_NOT_CONFIRMED")
g={"status":"V12_ALPHA_OPERATING_LOOP_ENTRY_BLOCKED","ready_for_alpha_operating_loop":False,"blocking_reasons":reasons,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(g,open(C/"v12_alpha_operating_loop_entry_gate.json","w"),indent=2)
print(f"V12: BLOCKED | reasons={reasons}")
