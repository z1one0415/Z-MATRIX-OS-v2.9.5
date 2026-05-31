#!/usr/bin/env python3
"""V6-B entry gate — check if price-only factor calculation is allowed."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
inv=json.loads((C/"v6a_factor_input_inventory.json").read_text())
mat=json.loads((C/"core_12_factor_requirement_matrix.json").read_text())
price_ok=mat["core_12_cases"]==12
price_factors=inv["real_ready_count"]+inv["partial_ready_count"]
syn_ok=inv["synthetic_blocked_count"]>=1
ready=price_ok and price_factors>=5 and syn_ok
g={"status":"V6B_PRICE_ONLY_FACTOR_ENTRY_ALLOWED" if ready else "V6B_ENTRY_BLOCKED",
   "core_12_price_inputs_ready":12,"price_only_factor_ready_count":price_factors,
   "financial_factor_ready_count":0,"valuation_factor_ready_count":0,
   "synthetic_factor_allowed_count":0,"ready_for_v6b_price_only_calculation":ready,
   "ready_for_factor_validation":False,"ready_for_alpha_claim":False,
   "blocking_reasons":[],"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
(C/"v6b_price_only_factor_entry_gate.json").write_text(json.dumps(g,indent=2,ensure_ascii=False))
print("V6-B Entry: "+("ALLOWED" if ready else "BLOCKED")+" | factors:"+str(price_factors))
