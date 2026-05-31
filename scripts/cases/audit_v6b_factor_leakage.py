#!/usr/bin/env python3
"""V6-C: Leakage audit — no future data, no forward return as factor, no alpha claims."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
data=json.loads((C/"v6b_price_only_factor_values.json").read_text())
fut=0; inp=0; fwd=0; alp=0; total=0
for r in data["records"]:
    for fid,f in r["factor_values"].items():
        total+=1
        if f.get("uses_future_data",False): fut+=1
        if f.get("input_end_date","9999")>f.get("as_of_date","0000"): inp+=1
    if r.get("ready_for_alpha_claim"): alp+=1
for r in data["records"]:
    for fid in r["factor_values"]:
        for fb in ["FORWARD_RETURN","FUTURE_RETURN","FWD_RETURN"]:
            if fb in fid.upper(): fwd+=1
safe=fut==0 and inp==0 and fwd==0
audit={"status":"V6B_FACTOR_LEAKAGE_AUDIT_PASS" if safe else "V6B_FACTOR_LEAKAGE_AUDIT_FAIL",
       "factor_records_checked":total,"future_data_violations":fut,
       "input_date_violations":inp,"forward_return_as_factor_violations":fwd,
       "alpha_claim_violations":alp,"leakage_safe":safe}
(C/"v6b_factor_leakage_audit.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False))
print(f"Leakage: safe={safe} future={fut} input_date={inp} fwd_as_factor={fwd}")
