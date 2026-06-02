#!/usr/bin/env python3
"""V11.5-C: Run paper portfolio simulation."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
sn=json.loads((C/"v11_paper_signal_snapshot.json").read_text())
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
lab={}
for l in lb["labels"]:lab[(l["as_of_date"],l["ticker"],l["horizon"])]=l
eligible=[s for s in sn["snapshots"]if s.get("rankic_direction")in("NEGATIVE","POSITIVE")and s.get("favored_bucket_size",0)>0]
results=[]
for s in eligible:
    fav=s.get("favored_bucket",[]);comp=s.get("comparison_bucket",[])
    for hn in["T20","T60"]:
        fr=[lab.get((s["as_of_date"],tk,hn),{}).get("future_relative_return",0)for tk in fav];cr=[lab.get((s["as_of_date"],tk,hn),{}).get("future_relative_return",0)for tk in comp]
        fa=sum(fr)/len(fr)if fr else None;ca=sum(cr)/len(cr)if cr else None
        spv=(fa-ca)if(fa is not None and ca is not None)else None
        results.append({"watch_id":s["watch_id"],"factor_id":s["factor_id"],"horizon":hn,"rankic_direction":s["rankic_direction"],"favored_bucket_return":round(fa,6)if fa else None,"comparison_bucket_return":round(ca,6)if ca else None,"bucket_spread":round(spv,6)if spv else None,"paper_only":True,"investment_action":"NONE"})
sim={"status":"V11_5_PAPER_PORTFOLIO_SIMULATION_BUILT","simulation_mode":"PAPER_ONLY","portfolio_count":len(eligible),"results":results,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(sim,open(C/"v11_5_paper_portfolio_simulation.json","w"),indent=2)
print(f"Simulation: {len(eligible)} portfolios, {len(results)} results")
