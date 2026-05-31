#!/usr/bin/env python3
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
RD=W/"runtime_reports"/"cases"/"core_12_real_market_data_readiness.json"
RR=W/"runtime_reports"/"cases"/"core_12_real_return_readiness.json"
def main():
    rd=json.loads(RD.read_text()) if RD.exists() else {"summary":{}}
    rr=json.loads(RR.read_text()) if RR.exists() else {"summary":{}}
    dp=rd["summary"].get("daily_price_real",0)
    ar=rd["summary"].get("adjustment_ready",0)
    br=rd["summary"].get("benchmark_local",False)
    cr=rd["summary"].get("calendar_local",False)
    rr2=rr["summary"].get("ready_for_real_return",0)
    al=rr["summary"].get("ready_for_alpha_claim",0)
    bl=[]
    if dp<12: bl.append("DAILY_PRICE_NOT_12")
    if ar<12: bl.append("ADJUSTMENT_FACTOR_NOT_READY")
    if not br: bl.append("BENCHMARK_NOT_REAL")
    if not cr: bl.append("CALENDAR_NOT_REAL")
    if rr2<12: bl.append("REAL_RETURN_NOT_READY")
    if al>0: bl.append("ALPHA_CLAIM_NOT_ZERO")
    rd2=len(bl)==0
    g={"status":"V5_ENTRY_ALLOWED" if rd2 else "V5_ENTRY_BLOCKED_WAITING_USER_MARKET_DATA","daily_price_real_read_only":dp,"adjustment_factor_ready":ar,"benchmark_real_read_only":br,"calendar_real_read_only":cr,"ready_for_real_return":rr2,"ready_for_alpha_claim":al,"v5_entry_allowed":rd2,"blocking_reasons":bl,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    (W/"runtime_reports"/"cases"/"v5_entry_gate.json").write_text(json.dumps(g,indent=2,ensure_ascii=False))
    print("V5: "+("ALLOWED" if rd2 else "BLOCKED")+" | P:"+str(dp)+"/12 A:"+str(ar)+"/12 B:"+str(br)+" C:"+str(cr)+" R:"+str(rr2)+"/12 Reasons:"+str(bl))
if __name__=="__main__": main()
