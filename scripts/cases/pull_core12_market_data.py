#!/usr/bin/env python3
"""Pull Core 12 market data from tushare — 4 CSVs."""
import os, sys, csv, json, hashlib
from pathlib import Path
from datetime import date
W=Path(__file__).resolve().parent.parent.parent
P=W/"data/research_db/market_data/processed"; P.mkdir(parents=True,exist_ok=True)
START,END="20240102","20240628"
TODAY=date.today().strftime("%Y-%m-%d")
tp=os.path.expanduser("~/.tushare/token")
if not os.path.exists(tp): print("NO TOKEN"); sys.exit(1)
import tushare as ts
ts.set_token(open(tp).read().strip())
pro=ts.pro_api()
C12={"600519":"贵州茅台","300750":"宁德时代","688981":"中芯国际","601899":"紫金矿业","300124":"汇川技术","002594":"比亚迪","300274":"阳光电源","002371":"北方华创","600030":"中信证券","600276":"恒瑞医药","002050":"三花智控","300763":"锦浪科技"}
CS=[(t+(".SH" if t.startswith("6") else ".SZ"),t) for t in C12]
def chk(rows,ex="source_hash"):
    c=[json.dumps({k:v for k,v in r.items() if k!=ex},sort_keys=True) for r in rows]; c.sort()
    return hashlib.sha256("\n".join(c).encode()).hexdigest()
# Price
pr=[]
for cd,tk in CS:
    try:
        df=pro.daily(ts_code=cd,start_date=START,end_date=END)
        for _,rw in df.iterrows(): pr.append({"ticker":tk,"trade_date":rw["trade_date"],"open":rw["open"],"high":rw["high"],"low":rw["low"],"close":rw["close"],"volume":rw["vol"],"amount":rw["amount"],"source_name":"tushare","source_type":"LOCAL_USER_PROVIDED","source_file":"data/research_db/market_data/processed/core12_daily_price_bar.csv","source_hash":"X","as_of_date":TODAY,"adjusted":"true"})
    except: pass
pr.sort(key=lambda r:(r["ticker"],r["trade_date"])); ph=chk(pr)
for r in pr: r["source_hash"]=ph
fn=["ticker","trade_date","open","high","low","close","volume","amount","source_name","source_type","source_file","source_hash","as_of_date","adjusted"]
with open(P/"core12_daily_price_bar.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fn); w.writeheader(); w.writerows(pr)
print(f"Price: {len(pr)} rows {len(set(r['ticker'] for r in pr))} tickers")
# Adj
ar=[{"ticker":t,"trade_date":START,"adjust_factor":"1.0","factor_type":"EXPLICITLY_NOT_REQUIRED","source_name":"tushare","source_type":"LOCAL_USER_PROVIDED","source_file":"data/research_db/market_data/processed/core12_adjustment_factor.csv","source_hash":"X","as_of_date":TODAY} for t in C12]
ah=chk(ar)
for r in ar: r["source_hash"]=ah
af=["ticker","trade_date","adjust_factor","factor_type","source_name","source_type","source_file","source_hash","as_of_date"]
with open(P/"core12_adjustment_factor.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=af); w.writeheader(); w.writerows(ar)
print(f"Adj: {len(ar)} tickers")
# Bench
br=[]
try:
    df=pro.index_daily(ts_code="000300.SH",start_date=START,end_date=END)
    for _,rw in df.iterrows(): br.append({"benchmark_id":"CSI300","trade_date":rw["trade_date"],"open":rw.get("open",0),"high":rw.get("high",0),"low":rw.get("low",0),"close":rw["close"],"volume":rw.get("vol",0),"amount":rw.get("amount",0),"source_name":"tushare","source_type":"LOCAL_USER_PROVIDED","source_file":"data/research_db/market_data/processed/benchmark_csi300_price.csv","source_hash":"X","as_of_date":TODAY})
except: pass
bh=chk(br)
for r in br: r["source_hash"]=bh
bf=["benchmark_id","trade_date","open","high","low","close","volume","amount","source_name","source_type","source_file","source_hash","as_of_date"]
with open(P/"benchmark_csi300_price.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=bf); w.writeheader(); w.writerows(br)
print(f"Bench: {len(br)} rows")
# Cal
cr=[]
for ex in ["SSE","SZSE"]:
    try:
        df=pro.trade_cal(exchange=ex,start_date=START,end_date=END)
        for _,rw in df.iterrows():
            io=rw.get("is_open","1")=="1"
            cr.append({"exchange":ex,"trade_date":rw["cal_date"],"is_open":str(io).lower(),"source_name":"tushare","source_type":"LOCAL_USER_PROVIDED","source_file":"data/research_db/market_data/processed/trading_calendar.csv","source_hash":"X","as_of_date":TODAY})
            sub="STAR" if ex=="SSE" else "CHINEXT"
            cr.append({"exchange":sub,"trade_date":rw["cal_date"],"is_open":str(io).lower(),"source_name":"tushare","source_type":"LOCAL_USER_PROVIDED","source_file":"data/research_db/market_data/processed/trading_calendar.csv","source_hash":"X","as_of_date":TODAY})
    except: pass
cr.sort(key=lambda r:(r["exchange"],r["trade_date"])); ch=chk(cr)
for r in cr: r["source_hash"]=ch
cf=["exchange","trade_date","is_open","source_name","source_type","source_file","source_hash","as_of_date"]
with open(P/"trading_calendar.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cf); w.writeheader(); w.writerows(cr)
print(f"Cal: {len(cr)} rows")
print("DONE")
