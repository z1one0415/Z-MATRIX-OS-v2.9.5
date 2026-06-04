#!/usr/bin/env python3
"""V11.6.1: Build OOS completion contract."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
reg=json.loads((C/"v11_6_tracking_registry.json").read_text())
sim=json.loads((C/"v11_5_paper_portfolio_simulation.json").read_text())
results=[]
t20c=0;t60c=0;t20t=0;t60t=0
for obs in reg["observations"]:
    fid=obs["factor_id"];h=obs["horizon"]
    if h=="T20":t20t+=1
    else:t60t+=1
    sr=next((r for r in sim["results"]if r["factor_id"]==fid and r["horizon"]==h),{})
    ok=sr.get("calculation_status")=="CALCULATED"
    if ok:
        if h=="T20":t20c+=1
        else:t60c+=1
    results.append(dict(observation_id=obs["observation_id"],factor_id=fid,horizon=h,completion_status="COMPLETED"if ok else"WAITING_FOR_LABEL",paper_only=True,investment_action="NONE"))
all_ok=(t20c==t20t and t60c==t60t)
ct=dict(status="V11_6_1_OOS_COMPLETION_ENGINE_BUILT",total_observations=len(results),t20_complete=t20c,t20_target=t20t,t60_complete=t60c,t60_target=t60t,overall_completion_ratio=(t20c+t60c)/len(results)if results else 0,paper_tracking_period_completed=all_ok,observations=results,ready_for_v12=all_ok,ready_for_alpha_claim=False,alpha_validated=False,production="BLOCKED",broker_runtime="BLOCKED",real_trade="BLOCKED")
json.dump(ct,open(C/"v11_6_1_oos_completion_contract.json","w"),indent=2)
print(f"OOS Completion: T20={t20c}/{t20t} T60={t60c}/{t60t} done={all_ok}")
