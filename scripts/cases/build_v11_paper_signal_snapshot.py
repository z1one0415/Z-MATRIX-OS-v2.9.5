#!/usr/bin/env python3
"""V11-C: Build paper signal snapshot from latest V8 factor values."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"; L=W/"runtime_reports/cases/v8_large_data"
fv=json.loads((L/"v8_expanded_factor_values.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
ad=max(r["as_of_date"] for r in fv["records"])
snaps=[]
for wi in wl["watch_items"]:
    fid=wi["factor_id"];rd=wi["rankic_direction"]
    vals=[]; 
    for r in fv["records"]:
        if r["as_of_date"]==ad and fid in r.get("factor_values",{}): vals.append((r["ticker"],r["factor_values"][fid]["value"]))
    vals.sort(key=lambda x:x[1]);n=len(vals)
    bot=[t for t,v in vals[:max(1,n//5)]];top=[t for t,v in vals[-max(1,n//5):]]
    interp="Lower values favored (NEGATIVE RankIC)" if rd=="NEGATIVE" else("Higher values favored (POSITIVE RankIC)" if rd=="POSITIVE" else"MIXED: no preferred direction")
    snaps.append({"watch_id":wi["watch_id"],"factor_id":fid,"horizon":wi["horizon"],"rankic_direction":rd,"as_of_date":ad,"universe_count":n,"signal_interpretation":interp,"favored_bucket_size":len(bot if rd=="NEGATIVE" else top),"comparison_bucket_size":len(top if rd=="NEGATIVE" else bot),"bucket_policy":"OBSERVATION_ONLY_NO_TRADE","investment_action":"NONE"})
s={"status":"V11_PAPER_SIGNAL_SNAPSHOT_BUILT","as_of_date":ad,"candidate_factor_count":len(snaps),"universe_count":len(set(r["ticker"] for r in fv["records"])),"snapshots":snaps,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(s,open(C/"v11_paper_signal_snapshot.json","w"),indent=2)
print(f"Signal snapshot: {len(snaps)} @ {ad}")
