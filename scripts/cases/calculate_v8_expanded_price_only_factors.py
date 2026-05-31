#!/usr/bin/env python3
"""V8-D: Calculate expanded (71 stocks) trailing price-only factors."""
import json, csv, io, math, hashlib, os
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
PROC=W/"data/research_db/market_data/processed"; LARGE=W/"runtime_reports/cases/v8_large_data"
LARGE.mkdir(parents=True,exist_ok=True)
FACTORS={"MOM_1D":1,"MOM_5D":5,"MOM_10D":10,"MOM_20D":20,"MOM_60D":60,"REV_1D":1,"REV_5D":5,"VOLATILITY_20D":20,"VOLATILITY_60D":60,"MAX_DRAWDOWN_60D":60,"TRAILING_BENCHMARK_RELATIVE_20D":20,"TRAILING_BENCHMARK_RELATIVE_60D":60,"VOLUME_20D_AVG":20,"VOLUME_60D_AVG":60,"AMOUNT_20D_AVG":20,"AMOUNT_60D_AVG":60}
p={};v={};a={}
for r in csv.DictReader(io.StringIO((PROC/"v8_expanded_daily_price_bar.csv").read_text())):
    t,d=r["ticker"],r["trade_date"]; p.setdefault(t,{})[d]=float(r["close"]); v.setdefault(t,{})[d]=float(r["volume"]); a.setdefault(t,{})[d]=float(r["amount"])
b={}
for r in csv.DictReader(io.StringIO((PROC/"v8_benchmark_csi300_price.csv").read_text())): b[r["trade_date"]]=float(r["close"])
td=sorted(set(r["trade_date"] for r in csv.DictReader(io.StringIO((PROC/"v8_expanded_daily_price_bar.csv").read_text()))))
tks=sorted(p.keys()); ads=td[60:]
def stdv(v2):
    if len(v2)<2: return None
    m=sum(v2)/len(v2); return math.sqrt(sum((x-m)**2 for x in v2)/(len(v2)-1))
recs=[]
for ad in ads:
    i=td.index(ad)
    for tk in tks:
        ps=p.get(tk,{}); vs=v.get(tk,{}); am=a.get(tk,{}); fv={}
        for fid,n in FACTORS.items():
            st=i-n+1; if st<0: continue; wd=td[st:i+1]
            istart=td[i-n] if (fid.startswith("MOM_") or fid.startswith("TRAILING_BENCHMARK_RELATIVE_") or fid in ("REV_1D","REV_5D")) else td[st]
            if fid.startswith("MOM_"): pc=ps.get(td[st-1]); cc=ps.get(ad); val=(cc/pc-1) if pc and cc and pc>0 else None
            elif fid=="REV_1D": pc=ps.get(td[i-1]); cc=ps.get(ad); m=(cc/pc-1) if pc and cc and pc>0 else None; val=-m if m is not None else None
            elif fid=="REV_5D": s5=i-5; pc=ps.get(td[s5]) if s5>=0 else None; cc=ps.get(ad); m=(cc/pc-1) if pc and cc and pc>0 else None; val=-m if m is not None else None
            elif fid.startswith("VOLATILITY_"): dr=[]; prev=None
                for d in wd: cm=ps.get(d)
                    if prev and cm and prev>0: dr.append(cm/prev-1); prev=cm
                val=stdv(dr) if dr else None
            elif fid=="MAX_DRAWDOWN_60D": pk=-1e9; md=1.0
                for d in wd: cl=ps.get(d)
                    if cl is None: continue
                    if cl>pk: pk=cl
                    if pk>0: md=min(md,cl/pk-1); val=md if md<1.0 else 0.0
            elif fid.startswith("TRAILING_BENCHMARK_RELATIVE_"): ps2=ps.get(td[st-1]); cs2=ps.get(ad); pb=b.get(td[st-1]); cb=b.get(ad); val=(cs2/ps2-1)-(cb/pb-1) if ps2 and cs2 and ps2>0 and pb and cb and pb>0 else None
            elif fid.startswith("VOLUME_"): vl=[vs.get(d) for d in wd if vs.get(d) is not None]; val=sum(vl)/len(vl) if vl else None
            elif fid.startswith("AMOUNT_"): al=[am.get(d) for d in wd if am.get(d) is not None]; val=sum(al)/len(al) if al else None
            else: val=None
            if val is not None: fv[fid]={"value":round(val,10),"truth_status":"REAL_READ_ONLY","lookback_days":n,"input_start_date":istart,"input_end_date":ad,"as_of_date":ad,"uses_future_data":False}
        if fv: recs.append({"as_of_date":ad,"ticker":tk,"factor_values":fv,"ready_for_alpha_claim":False})
j=json.dumps({"status":"V8_EXPANDED_FACTOR_VALUES_CALCULATED","factor_count":len(FACTORS),"stock_count":len(tks),"as_of_date_count":len(ads),"records":recs},ensure_ascii=False)
fp=LARGE/"v8_expanded_factor_values.json"; fp.write_text(j)
fh=hashlib.sha256(j.encode()).hexdigest(); sz=os.path.getsize(fp)
nv=sum(len(r["factor_values"]) for r in recs); ex=len(ads)*len(tks)*len(FACTORS)
summary={"status":"SUMMARY_ONLY","factor_records":len(recs),"factor_values":nv,"coverage":round(nv/ex,4),"large_file_hash":fh[:16],"large_file_size_mb":round(sz/1024/1024,1)}
json.dump(summary,open(W/"runtime_reports/cases/v8_expanded_factor_values_summary.json","w"),indent=2)
print(f"Factor rebuild: {len(recs)} records, {nv} values, coverage={nv/ex:.4f}, hash={fh[:16]}")
