#!/usr/bin/env python3
"""V9-A: Calculate formal IC/RankIC stability from V8 large data."""
import json, math
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
LARGE=W/"runtime_reports/cases/v8_large_data"; C=W/"runtime_reports/cases"
factors=json.loads((LARGE/"v8_expanded_factor_values.json").read_text())
labels=json.loads((LARGE/"v8_forward_return_labels.json").read_text())
# Pre-index
fv_by={(r["as_of_date"],r["ticker"]):r["factor_values"] for r in factors["records"]}
lab_by={(l["as_of_date"],l["ticker"],l["horizon"]):l["future_relative_return"] for l in labels["labels"]}
fids=sorted(list(next(iter(fv_by.values())).keys()))
hn=["T1","T5","T10","T20","T60"]
ads=sorted(set(r["as_of_date"] for r in factors["records"]))
tickers=sorted(set(r["ticker"] for r in factors["records"]))
def pearson(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sx=math.sqrt(sum((x-mx)**2 for x in xs)/(n-1)) if n>1 else 0
    sy=math.sqrt(sum((y-my)**2 for y in ys)/(n-1)) if n>1 else 0
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/((n-1)*sx*sy) if sx and sy else None
def spearman(xs,ys):
    ux=sorted(set(xs)); uy=sorted(set(ys))
    rx={v:i for i,v in enumerate(ux)}; ry={v:i for i,v in enumerate(uy)}
    return pearson([rx[x] for x in xs],[ry[y] for y in ys])
results=[]
for fid in fids:
    for h in hn:
        ics=[]; rics=[]; css=[]
        for ad in ads:
            xs=[]; ys=[]
            for tk in tickers:
                fv=fv_by.get((ad,tk)); yv=lab_by.get((ad,tk,h))
                if fv and fid in fv and yv is not None: xs.append(fv[fid]["value"]); ys.append(yv)
            if len(xs)<30: continue
            ic=pearson(xs,ys); ric=spearman(xs,ys)
            if ic is not None: ics.append(ic)
            if ric is not None: rics.append(ric)
            css.append(len(xs))
        if not rics: continue
        n=len(rics); m=sum(rics)/n; s=math.sqrt(sum((x-m)**2 for x in rics)/(n-1)) if n>1 else 0
        mic=sum(ics)/len(ics) if ics else 0; sic=math.sqrt(sum((x-mic)**2 for x in ics)/(len(ics)-1)) if len(ics)>1 else 0
        ok=n>=250
        results.append({"factor_id":fid,"horizon":h,"valid_date_count":n,"average_cross_section_size":round(sum(css)/len(css),1),"min_cross_section_size":min(css),"max_cross_section_size":max(css),"mean_ic":round(mic,6),"median_ic":round(sorted(ics)[len(ics)//2],6),"ic_std":round(sic,6),"icir":round(abs(mic)/sic,4) if sic>0 else None,"positive_ic_ratio":round(sum(1 for v in ics if v>0)/len(ics),4),"mean_rankic":round(m,6),"median_rankic":round(sorted(rics)[n//2],6),"rankic_std":round(s,6),"rankic_ir":round(abs(m)/s,4) if s>0 else None,"positive_rankic_ratio":round(sum(1 for v in rics if v>0)/n,4),"formal_sample_status":"SUFFICIENT" if ok else "INSUFFICIENT_SAMPLE","ready_for_selection_gate":ok,"ready_for_alpha_claim":False,"alpha_validated":False})
json.dump({"status":"V9_FORMAL_FACTOR_STABILITY_BUILT","validation_type":"FORMAL_STABILITY_VALIDATION_NON_TRADING","factor_count":len(fids),"horizon_count":len(hn),"factor_horizon_count":len(results),"label_type":"future_relative_return","min_cross_section_size_required":30,"min_valid_date_count_required":250,"alpha_validated":False,"ready_for_alpha_claim":False,"metrics":results},open(C/"v9_formal_factor_stability.json","w"),indent=2)
print(f"Stability: {len(results)} factor×horizon metrics")
