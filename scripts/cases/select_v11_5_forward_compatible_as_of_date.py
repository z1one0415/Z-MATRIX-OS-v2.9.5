#!/usr/bin/env python3
"""Select forward-compatible historical as_of_date for V11.5 simulation."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
fv=json.loads((L/"v8_expanded_factor_values.json").read_text())
t60={l["as_of_date"]for l in lb["labels"]if l["horizon"]=="T60"}
t20={l["as_of_date"]for l in lb["labels"]if l["horizon"]=="T20"}
adt=sorted(set(r["as_of_date"]for r in fv["records"]))
comp=sorted(d for d in adt if d in t60 and d in t20)
ready=len(comp)>=60
sel=comp[-60]if ready else(comp[0]if comp else None)
d={"status":"V11_5_FORWARD_COMPATIBLE_AS_OF_DATE_SELECTED"if ready else"V11_5_FORWARD_COMPATIBLE_AS_OF_DATE_BLOCKED","selected_as_of_date":sel,"required_horizons":["T20","T60"],"total_compatible_dates":len(comp),"ready_for_historical_snapshot":ready}
json.dump(d,open(C/"v11_5_forward_compatible_as_of_date.json","w"),indent=2)
print(f"As-of-date: {sel} | compatible_dates={len(comp)} | ready={ready}")
