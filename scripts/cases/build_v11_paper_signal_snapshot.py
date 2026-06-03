#!/usr/bin/env python3
"""Build signal snapshot at forward-compatible historical date."""
import json,math
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
sel=json.loads((C/"v11_5_forward_compatible_as_of_date.json").read_text())
fv_data=json.loads((L/"v8_expanded_factor_values.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
latest_ad=sel.get("selected_as_of_date")or max(r["as_of_date"]for r in fv_data["records"])
is_full=sel.get("ready_for_full_portfolio_simulation",False)
snaps=[]
for wi in wl["watch_items"]:
    fid=wi["factor_id"];rd=wi["rankic_direction"];vs=[]
    for r in fv_data["records"]:
        if r["as_of_date"]==latest_ad and fid in r.get("factor_values",{}):
            vs.append((r["ticker"],r["factor_values"][fid]["value"]))
    vs.sort(key=lambda x:x[1]);n=len(vs)
    if rd=="NEGATIVE":
        bot=[t for t,v in vs[:max(1,n//5)]];top=[t for t,v in vs[-max(1,n//5):]]
        s={"favored_bucket":bot,"comparison_bucket":top,"favored_bucket_size":len(bot),"comparison_bucket_size":len(top),"bucket_direction":"LOW_FACTOR_VALUE_FAVORED","bucket_policy":"OBSERVATION_ONLY_NO_TRADE","signal_interpretation":"Lower values favored under NEGATIVE RankIC."}
    elif rd=="POSITIVE":
        top=[t for t,v in vs[-max(1,n//5):]];bot=[t for t,v in vs[:max(1,n//5)]]
        s={"favored_bucket":top,"comparison_bucket":bot,"favored_bucket_size":len(top),"comparison_bucket_size":len(bot),"bucket_direction":"HIGH_FACTOR_VALUE_FAVORED","bucket_policy":"OBSERVATION_ONLY_NO_TRADE","signal_interpretation":"Higher values favored under POSITIVE RankIC."}
    else:
        s={"favored_bucket":[],"comparison_bucket":[],"favored_bucket_size":0,"comparison_bucket_size":0,"bucket_direction":"NO_PREFERRED_DIRECTION","bucket_policy":"OBSERVATION_ONLY_NO_PREFERRED_DIRECTION","signal_interpretation":"MIXED: no preferred bucket."}
    snaps.append({"watch_id":wi["watch_id"],"factor_id":fid,"horizon":wi["horizon"],"rankic_direction":rd,"as_of_date":latest_ad,"universe_count":n,**s,"investment_action":"NONE"})
sn={"status":"V11_PAPER_SIGNAL_SNAPSHOT_BUILT","as_of_date":latest_ad,"as_of_date_policy":"HISTORICAL_FORWARD_COMPATIBLE"if is_full else"LATEST_AVAILABLE","forward_compatible":is_full,"selector_coverage_mode":sel.get("coverage_mode","UNKNOWN"),"snapshots":snaps,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(sn,open(C/"v11_paper_signal_snapshot.json","w"),indent=2)
print(f"Snapshot: {latest_ad} fwd={is_full} mode={sel.get('coverage_mode')}")
