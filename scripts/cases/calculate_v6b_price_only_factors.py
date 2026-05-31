#!/usr/bin/env python3
"""V6-B: Calculate 16 trailing price-only factors from real CSV data."""
import json, csv, io, math
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
PROC = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"

FACTORS = {
    "MOM_1D":1,"MOM_5D":5,"MOM_10D":10,"MOM_20D":20,"MOM_60D":60,
    "REV_1D":1,"REV_5D":5,
    "VOLATILITY_20D":20,"VOLATILITY_60D":60,
    "MAX_DRAWDOWN_60D":60,
    "TRAILING_BENCHMARK_RELATIVE_20D":20,"TRAILING_BENCHMARK_RELATIVE_60D":60,
    "VOLUME_20D_AVG":20,"VOLUME_60D_AVG":60,
    "AMOUNT_20D_AVG":20,"AMOUNT_60D_AVG":60,
}

def main():
    prices={}; volumes={}; amounts={}
    for row in csv.DictReader(io.StringIO((PROC/"core12_daily_price_bar.csv").read_text())):
        t,d=row["ticker"],row["trade_date"]
        prices.setdefault(t,{})[d]=float(row["close"])
        volumes.setdefault(t,{})[d]=float(row["volume"])
        amounts.setdefault(t,{})[d]=float(row["amount"])
    
    bench={}
    for row in csv.DictReader(io.StringIO((PROC/"benchmark_csi300_price.csv").read_text())):
        bench[row["trade_date"]]=float(row["close"])
    
    td=sorted(prices.get("600519",{}).keys())
    REG=json.loads((W/"data/research_db/cases/case_registry_v1.json").read_text())
    CORE=[c for c in REG if c.get("case_layer")=="CORE"]
    ads=td[60:]
    
    def stdv(vals):
        if len(vals)<2: return None
        m=sum(vals)/len(vals)
        return math.sqrt(sum((x-m)**2 for x in vals)/(len(vals)-1))
    
    records=[]
    for ad in ads:
        i=td.index(ad)
        for c in CORE:
            tk=c["ticker"]; ps=prices.get(tk,{}); vs=volumes.get(tk,{}); am=amounts.get(tk,{}); fv={}
            for fid,n in FACTORS.items():
                st=i-n+1
                if st<0: continue
                wd=td[st:i+1]; istart=td[st]; iend=ad
                if fid.startswith("MOM_"):
                    pc=ps.get(td[st-1]); cc=ps.get(ad)
                    val=(cc/pc-1) if pc and cc and pc>0 else None
                elif fid=="REV_1D":
                    pc=ps.get(td[i-1]); cc=ps.get(ad)
                    m=(cc/pc-1) if pc and cc and pc>0 else None; val=-m if m is not None else None
                elif fid=="REV_5D":
                    s5=i-5; pc=ps.get(td[s5]) if s5>=0 else None; cc=ps.get(ad)
                    m=(cc/pc-1) if pc and cc and pc>0 else None; val=-m if m is not None else None
                elif fid.startswith("VOLATILITY_"):
                    dr=[]; prev=None
                    for d in wd:
                        cm=ps.get(d)
                        if prev and cm and prev>0: dr.append(cm/prev-1)
                        prev=cm
                    val=stdv(dr) if dr else None
                elif fid=="MAX_DRAWDOWN_60D":
                    pk=-1e9; md=1.0
                    for d in wd:
                        cl=ps.get(d)
                        if cl is None: continue
                        if cl>pk: pk=cl
                        if pk>0: md=min(md,cl/pk-1)
                    val=md if md<1.0 else 0.0
                elif fid.startswith("TRAILING_BENCHMARK_RELATIVE_"):
                    ps2=ps.get(td[st-1]); cs2=ps.get(ad)
                    pb=bench.get(td[st-1]); cb=bench.get(ad)
                    if ps2 and cs2 and ps2>0 and pb and cb and pb>0:
                        val=(cs2/ps2-1)-(cb/pb-1)
                    else: val=None
                elif fid.startswith("VOLUME_"):
                    vl=[vs.get(d) for d in wd if vs.get(d) is not None]
                    val=sum(vl)/len(vl) if vl else None
                elif fid.startswith("AMOUNT_"):
                    al=[am.get(d) for d in wd if am.get(d) is not None]
                    val=sum(al)/len(al) if al else None
                else: val=None
                if val is not None:
                    fv[fid]={
                        "value":round(val,10),"truth_status":"REAL_READ_ONLY",
                        "lookback_days":n,"input_start_date":istart,"input_end_date":iend,
                        "as_of_date":ad,"uses_future_data":False,
                        "calculation_formula":f"trailing_{fid}",
                    }
            if fv:
                records.append({
                    "as_of_date":ad,"case_id":c["case_id"],"ticker":tk,"name":c["name"],
                    "factor_values":fv,"ready_for_alpha_claim":False,
                })
    out={"status":"V6B_PRICE_ONLY_FACTOR_VALUES_CALCULATED","factor_count":len(FACTORS),
         "core_12_cases":len(CORE),"as_of_date_count":len(ads),
         "lookback_policy":"TRAILING_ONLY_NO_FUTURE_DATA",
         "as_of_date_range":[ads[0],ads[-1]],"records":records}
    (CASES/"v6b_price_only_factor_values.json").write_text(json.dumps(out,indent=2,ensure_ascii=False))
    nvals=sum(len(r["factor_values"]) for r in records)
    print(f"Factor values: {len(FACTORS)} factors x {len(CORE)} cases x {len(ads)} dates = {nvals} values")

if __name__=="__main__": main()
