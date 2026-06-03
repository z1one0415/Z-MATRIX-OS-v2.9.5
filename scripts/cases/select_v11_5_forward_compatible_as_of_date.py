#!/usr/bin/env python3
"""Select latest full-coverage forward-compatible as_of_date — strict 1.0, all dates."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
fv=json.loads((L/"v8_expanded_factor_values.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
lab_by={}
for l in lb["labels"]:lab_by[(l["as_of_date"],l["ticker"],l["horizon"])]=l
fv_by={}
for r in fv["records"]:fv_by.setdefault(r["as_of_date"],{})[r["ticker"]]=r.get("factor_values",{})
eligible=[w for w in wl["watch_items"]if w.get("watch_status")=="ACTIVE_PAPER_WATCH"]
all_dates=sorted(fv_by.keys())
best_date=None;best_e=0;best_f=0
for ad in all_dates:
    if ad not in fv_by:continue
    bt=set()
    for wi in eligible:
        fid=wi["factor_id"];rd=wi["rankic_direction"];vs=[]
        for tk,factors in fv_by[ad].items():
            if fid in factors:vs.append((tk,factors[fid]["value"]))
        vs.sort(key=lambda x:x[1]);n=len(vs)
        if n<10:continue
        if rd=="NEGATIVE":bt.update(t for t,v in vs[:max(1,n//5)])
        elif rd=="POSITIVE":bt.update(t for t,v in vs[-max(1,n//5):])
    e=0;f=0
    for hn in["T20","T60"]:
        for tk in bt:e+=1
        if(ad,tk,hn)in lab_by:f+=1
    cov=f/e if e>0 else 0
    if cov==1.0 and ad>str(best_date or""):best_date,best_e,best_f=ad,e,f
mode="FULL" if best_date else "PARTIAL"
d={"status":f"V11_5_FORWARD_COMPATIBLE_AS_OF_DATE_SELECTED_{mode}","selected_as_of_date":best_date,"coverage_mode":mode,"expected_label_count":best_e,"found_label_count":best_f,"missing_label_count":best_e-best_f,"coverage":1.0 if best_date else 0.0,"latest_full_coverage_selected":best_date is not None,"ready_for_full_portfolio_simulation":best_date is not None,"ready_for_partial_portfolio_report":True}
json.dump(d,open(C/"v11_5_forward_compatible_as_of_date.json","w"),indent=2)
print(f"Selector: {best_date} FULL={best_date is not None} e={best_e} f={best_f}")
