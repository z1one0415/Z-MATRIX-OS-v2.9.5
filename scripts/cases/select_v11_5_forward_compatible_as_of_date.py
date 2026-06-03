#!/usr/bin/env python3
"""Select forward-compatible as_of_date via label coverage check."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
fv=json.loads((L/"v8_expanded_factor_values.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
# Get snapshot tickers for coverage check
sn=json.loads((C/"v11_paper_signal_snapshot.json").read_text()) if (C/"v11_paper_signal_snapshot.json").exists() else {"snapshots":[]}
lab_by={}
for l in lb["labels"]:lab_by[(l["as_of_date"],l["ticker"],l["horizon"])]=l
# Test dates from existing data
test_dates=sorted(set(r["as_of_date"]for r in fv["records"]))[-200:]
best_date=None;best_cov=0
for ad in test_dates:
    # Count label coverage for snapshot tickers at this date
    e=0;f=0
    for s in sn.get("snapshots",[]):
        if s.get("rankic_direction")in("NEGATIVE","POSITIVE"):
            for bkt in["favored_bucket","comparison_bucket"]:
                for tk in s.get(bkt,[]):
                    for hn in["T20","T60"]:
                        e+=1
                        if(ad,tk,hn)in lab_by:f+=1
    if e==0:continue
    cov=f/e
    if cov>best_cov:best_date,best_cov=ad,cov
mode="FULL"if best_cov>=0.99 else"PARTIAL"
d={"status":f"V11_5_FORWARD_COMPATIBLE_AS_OF_DATE_SELECTED_{mode}","selected_as_of_date":best_date,"coverage_mode":mode,"coverage":round(best_cov,4),"ready_for_full_portfolio_simulation":mode=="FULL","ready_for_partial_portfolio_report":True}
json.dump(d,open(C/"v11_5_forward_compatible_as_of_date.json","w"),indent=2)
print(f"Selector: {best_date} coverage={best_cov:.4f} mode={mode}")
