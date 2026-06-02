#!/usr/bin/env python3
"""V11.5-F: Build V11.5 closeout."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
au=json.loads((C/"v11_5_paper_portfolio_risk_audit.json").read_text())
co={"status":"CASE_EXPANSION_V11_5_PAPER_PORTFOLIO_SIMULATION_CONFIRMED","portfolio_count":sim["portfolio_count"],"cost_model_status":"PROXY_ONLY","risk_audit_pass":au["status"]=="V11_5_PAPER_PORTFOLIO_RISK_AUDIT_PASS","ready_for_v12":False,"v12_blocking_reasons":au["v12_blocking_reasons"],"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(co,open(C/"case_expansion_v11_5_closeout.json","w"),indent=2)
print(f"Closeout: {co["status"]}")
