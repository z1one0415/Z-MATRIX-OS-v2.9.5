#!/usr/bin/env python3
"""Select latest full-coverage date — portfolio-level (per ticker/bucket/horizon)."""
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
best_date=None;best_e=0;best_f=0;best_rblk=0
for ad in all_dates:
    if ad not in fv_by:continue
    e=0;f=0;rblk=0
    # For each watch item, build buckets at this date
    for wi in eligible:
        fid=wi["factor_id"];rd=wi["rankic_direction"];vs=[]
        for tk,factors in fv_by[ad].items():
            if fid in factors:vs.append((tk,factors[fid]["value"]))
        vs.sort(key=lambda x:x[1]);n=len(vs)
        if n<10:continue
        # Build buckets (same logic as snapshot builder)
        if rd=="NEGATIVE":
            fav=[t for t,v in vs[:max(1,n//5)]];comp=[t for t,v in vs[-max(1,n//5):]]
            buckets=[("favored_bucket",fav),("comparison_bucket",comp)]
        elif rd=="POSITIVE":
            fav=[t for t,v in vs[-max(1,n//5):]];comp=[t for t,v in vs[:max(1,n//5)]]
            buckets=[("favored_bucket",fav),("comparison_bucket",comp)]
        else:continue
        # Per ticker, per bucket, per horizon counting
        for hn in["T20","T60"]:
            has_miss=False
            for bname,bkt in buckets:
                for tk in bkt:
                    e+=1
                    if(ad,tk,hn)in lab_by:f+=1
                    else:has_miss=True
            if has_miss:rblk+=1
    cov=f/e if e>0 else 0
    if cov==1.0 and ad>str(best_date or""):best_date,best_e,best_f,best_rblk=ad,e,f,rblk
mode="FULL"if best_date else"PARTIAL"
d={"status":f"V11_5_FORWARD_COMPATIBLE_AS_OF_DATE_SELECTED_{mode}","selected_as_of_date":best_date,"coverage_mode":mode,"expected_label_count":best_e,"found_label_count":best_f,"missing_label_count":best_e-best_f,"coverage":1.0 if best_date else 0.0,"result_level_expected":0,"result_level_calculable":0,"result_level_blocked":best_rblk,"latest_full_coverage_selected":best_date is not None,"ready_for_full_portfolio_simulation":best_date is not None,"ready_for_partial_portfolio_report":True,"selector_coverage_contract":"PORTFOLIO_LEVEL_WATCH_BUCKET_TICKER_HORIZON"}
json.dump(d,open(C/"v11_5_forward_compatible_as_of_date.json","w"),indent=2)
rr="result_level_expected"if best_date else""
print(f"Selector: {best_date} FULL={best_date is not None} e={best_e} f={best_f} rblk={best_rblk}")
