#!/usr/bin/env python3
"""V6-C Leakage audit: no future data, no forward return as factor, no alpha claims."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
data=json.loads((W/"runtime_reports/cases/v6b_price_only_factor_values.json").read_text())
fut=sum(1 for r in data["records"] for f in r["factor_values"].values() if f.get("uses_future_data",False))
alp=sum(1 for r in data["records"] if r.get("ready_for_alpha_claim"))
fwd=0
for r in data["records"]:
    for fid in r["factor_values"]:
        for fb in ["FORWARD_RETURN","FUTURE_RETURN","FWD_RETURN"]:
            if fb in fid.upper(): fwd+=1
safe=fut==0 and fwd==0
print(f"Leakage: safe={safe} future={fut} fwd_as_factor={fwd} alpha={alp}")
