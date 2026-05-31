#!/usr/bin/env python3
"""V8-E: Build expanded forward return labels."""
import json, csv, io, hashlib, os
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
PROC=W/"data/research_db/market_data/processed"; LARGE=W/"runtime_reports/cases/v8_large_data"
LARGE.mkdir(parents=True,exist_ok=True)
p={}
for r in csv.DictReader(io.StringIO((PROC/"v8_expanded_daily_price_bar.csv").read_text())): p.setdefault(r["ticker"],{})[r["trade_date"]]=float(r["close"])
b={}
for r in csv.DictReader(io.StringIO((PROC/"v8_benchmark_csi300_price.csv").read_text())): b[r["trade_date"]]=float(r["close"])
td=sorted(set(r["trade_date"] for r in csv.DictReader(io.StringIO((PROC/"v8_expanded_daily_price_bar.csv").read_text()))))
tks=sorted(p.keys()); ads=td[60:]
H={"T1":1,"T5":5,"T10":10,"T20":20,"T60":60}
labels=[]
for ad in ads:
    i=td.index(ad)
    for tk in tks:
        ps=p.get(tk,{})
        for hn,n in H.items():
            ti=i+n; if ti>=len(td): continue; fd=td[ti]; ec=ps.get(ad); xc=ps.get(fd); bc=b.get(ad); bx=b.get(fd)
            if not ec or not xc or ec<=0 or xc<=0: continue
            fsr=xc/ec-1; fbr=bx/bc-1 if bc and bx and bc>0 else None; frr=fsr-fbr if fbr is not None else None
            labels.append({"as_of_date":ad,"ticker":tk,"horizon":hn,"exit_date":fd,"future_stock_return":round(fsr,10),"future_relative_return":round(frr,10) if frr is not None else None,"label_status":"REAL_FORWARD_LABEL","used_as_factor_input":False})
j=json.dumps({"status":"V8_FORWARD_LABELS_BUILT","stock_count":len(tks),"label_records":len(labels),"labels":labels},ensure_ascii=False)
fp=LARGE/"v8_forward_return_labels.json"; fp.write_text(j)
fh=hashlib.sha256(j.encode()).hexdigest(); sz=os.path.getsize(fp)
json.dump({"status":"SUMMARY_ONLY","label_records":len(labels),"large_file_hash":fh[:16],"large_file_size_mb":round(sz/1024/1024,1)},open(W/"runtime_reports/cases/v8_forward_return_labels_summary.json","w"),indent=2)
print(f"Labels: {len(labels)} records, hash={fh[:16]}")
