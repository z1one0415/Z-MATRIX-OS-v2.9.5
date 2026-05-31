#!/usr/bin/env python3
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
RD=W/"runtime_reports"/"cases"/"core_12_real_market_data_readiness.json"
def main():
    if not RD.exists(): print("No readiness data"); return
    d=json.loads(RD.read_text())
    res=[]
    for c in d["cases"]:
        po=c["daily_price_status"] in ("REAL_READ_ONLY","PUBLIC_READ_ONLY","LOCAL_USER_PROVIDED")
        pf=c["daily_price_status"]=="FIXTURE"
        ao=c["adjustment_factor_status"] in ("REAL_READ_ONLY","PUBLIC_READ_ONLY","LOCAL_USER_PROVIDED","EXPLICITLY_NOT_REQUIRED")
        bo=c["benchmark_status"] in ("REAL_READ_ONLY","PUBLIC_READ_ONLY","LOCAL_USER_PROVIDED")
        co=c["calendar_status"] in ("REAL_READ_ONLY","PUBLIC_READ_ONLY","LOCAL_USER_PROVIDED")
        t20=c.get("t20_ready",False)
        res.append({"case_id":c["case_id"],"ticker":c["ticker"],"name":c["name"],"real_return_status":"READY" if (po and ao and t20) else ("BLOCKED_MISSING_ADJUSTMENT_FACTOR" if (po and not ao) else ("BLOCKED_FIXTURE_ONLY" if pf else ("BLOCKED_MISSING_PRICE" if not po else "BLOCKED_MISSING_CALENDAR"))),"fixture_return_ready":pf and co,"adjustment_factor_status":c["adjustment_factor_status"],"t20_return_ready":po and ao and t20,"t60_return_ready":po and ao and c.get("t60_ready",False),"real_alpha_status":"NOT_STARTED" if bo else "BLOCKED_NO_REAL_BENCHMARK","ready_for_real_return":po and ao and bo and co and t20,"ready_for_alpha_claim":False,"council_status":"BLOCKED_UNTIL_FACTOR_REAL","production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"})
    s={"total":len(res),"fixture_return_ready":sum(1 for r in res if r.get("fixture_return_ready")),"ready_for_real_return":sum(1 for r in res if r["ready_for_real_return"]),"ready_for_alpha_claim":0,"blocked_missing_adj":sum(1 for r in res if "ADJUSTMENT" in r.get("real_return_status","")),"blocked_missing_price":sum(1 for r in res if "PRICE" in r.get("real_return_status","")),"blocked_fixture_only":sum(1 for r in res if "FIXTURE" in r.get("real_return_status",""))}
    (W/"runtime_reports"/"cases"/"core_12_real_return_readiness.json").write_text(json.dumps({"schema_version":"v4.3","cases":res,"summary":s},indent=2,ensure_ascii=False))
    print(f"Return: {len(res)} cases Ready:{s['ready_for_real_return']}/12 AdjBlocked:{s['blocked_missing_adj']} Alpha:0")
if __name__=="__main__": main()
