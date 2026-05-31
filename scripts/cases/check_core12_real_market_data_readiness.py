#!/usr/bin/env python3
import json, csv, io
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
P = W / "data" / "research_db" / "market_data" / "processed"
REG = json.loads((W / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text())
def main():
    pf, af, bf, cf = P/"core12_daily_price_bar.csv", P/"core12_adjustment_factor.csv", P/"benchmark_csi300_price.csv", P/"trading_calendar.csv"
    pt = {}
    if pf.exists():
        for r in csv.DictReader(io.StringIO(pf.read_text())):
            t=r["ticker"]; d=r["trade_date"]
            pt.setdefault(t,{"min":d,"max":d,"cnt":0})
            if d<pt[t]["min"]: pt[t]["min"]=d
            if d>pt[t]["max"]: pt[t]["max"]=d
            pt[t]["cnt"]+=1
    at={}
    if af.exists():
        for r in csv.DictReader(io.StringIO(af.read_text())): at[r["ticker"]]=r.get("factor_type","EXPLICITLY_NOT_REQUIRED")
    be,ce=bf.exists(),cf.exists()
    res=[]
    for c in REG:
        if c.get("case_layer")!="CORE": continue
        t=c["ticker"]; pi=pt.get(t,{})
        hp=t in pt; ha=t in at; adj=at.get(t,"MISSING")
        res.append({"case_id":c["case_id"],"ticker":t,"name":c["name"],"daily_price_status":"LOCAL_USER_PROVIDED" if hp else "MISSING","daily_price_start":pi.get("min"),"daily_price_end":pi.get("max"),"trading_days":pi.get("cnt"),"t20_ready":hp,"t60_ready":hp,"adjustment_factor_status":adj if ha else "MISSING","benchmark_status":"LOCAL_USER_PROVIDED" if be else "MISSING","calendar_status":"LOCAL_USER_PROVIDED" if ce else "MISSING","fixture_return_ready":False,"ready_for_real_return":hp and ha and be and ce,"ready_for_alpha_claim":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"})
    s={"total":len(res),"daily_price_real":sum(1 for r in res if r["daily_price_status"]=="LOCAL_USER_PROVIDED"),"daily_price_fixture":0,"daily_price_missing":sum(1 for r in res if r["daily_price_status"]=="MISSING"),"adjustment_ready":sum(1 for r in res if r["adjustment_factor_status"]!="MISSING"),"benchmark_local":be,"calendar_local":ce,"ready_for_real_return":sum(1 for r in res if r["ready_for_real_return"]),"ready_for_alpha_claim":0}
    (W/"runtime_reports"/"cases"/"core_12_real_market_data_readiness.json").write_text(json.dumps({"schema_version":"v4.3","cases":res,"summary":s},indent=2,ensure_ascii=False))
    print(f"Readiness: {len(res)} cases Price:{s['daily_price_real']}/12 Adj:{s['adjustment_ready']}/12 Bench:{be} Cal:{ce} Return:{s['ready_for_real_return']}/12")
if __name__=="__main__": main()
