#!/usr/bin/env python3
"""V11.5-C: Run paper portfolio simulation — explicit label lookup, fail-closed on missing data."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
sn=json.loads((C/"v11_paper_signal_snapshot.json").read_text())
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
lab={}
for l in lb["labels"]:
    lab[(l["as_of_date"],l["ticker"],l["horizon"])]=l
eligible=[s for s in sn["snapshots"]if s.get("rankic_direction")in("NEGATIVE","POSITIVE")and s.get("favored_bucket_size",0)>0]
results=[]
null_return_count=0
blocked_result_count=0
calculated_result_count=0
missing_label_count=0
for s in eligible:
    fav=s.get("favored_bucket",[]);comp=s.get("comparison_bucket",[]);as_of=s["as_of_date"]
    for hn in["T20","T60"]:
        fr_vals=[];fr_miss=0
        for tk in fav:
            k=(as_of,tk,hn)
            if k in lab:fr_vals.append(lab[k]["future_relative_return"])
            else:fr_miss+=1
        cr_vals=[];cr_miss=0
        for tk in comp:
            k=(as_of,tk,hn)
            if k in lab:cr_vals.append(lab[k]["future_relative_return"])
            else:cr_miss+=1
        total_miss=fr_miss+cr_miss
        missing_label_count+=total_miss
        if total_miss>0 or len(fr_vals)==0 or len(cr_vals)==0:
            null_return_count+=1
            blocked_result_count+=1
            results.append({"watch_id":s["watch_id"],"factor_id":s["factor_id"],"horizon":hn,"rankic_direction":s["rankic_direction"],"favored_bucket_return":None,"comparison_bucket_return":None,"bucket_spread":None,"paper_only":True,"investment_action":"NONE","calculation_status":"BLOCKED_MISSING_FORWARD_LABELS","missing_favored_labels":fr_miss,"missing_comparison_labels":cr_miss})
            continue
        fa=sum(fr_vals)/len(fr_vals);ca=sum(cr_vals)/len(cr_vals)
        spv=fa-ca
        calculated_result_count+=1
        results.append({"watch_id":s["watch_id"],"factor_id":s["factor_id"],"horizon":hn,"rankic_direction":s["rankic_direction"],"favored_bucket_return":round(fa,6),"comparison_bucket_return":round(ca,6),"bucket_spread":round(spv,6),"paper_only":True,"investment_action":"NONE","calculation_status":"CALCULATED","missing_favored_labels":0,"missing_comparison_labels":0})
sim_completeness="FULL" if calculated_result_count>0 and blocked_result_count==0 and null_return_count==0 else ("PARTIAL" if calculated_result_count>0 else "BLOCKED")
sim={"status":"V11_5_PAPER_PORTFOLIO_SIMULATION_BUILT" if calculated_result_count>0 and blocked_result_count==0 and null_return_count==0 else ("V11_5_PAPER_PORTFOLIO_SIMULATION_PARTIAL" if calculated_result_count>0 else "V11_5_PAPER_PORTFOLIO_SIMULATION_BLOCKED"),"simulation_mode":"PAPER_ONLY","portfolio_count":len(eligible),"results":results,"null_return_count":null_return_count,"blocked_result_count":blocked_result_count,"calculated_result_count":calculated_result_count,"missing_label_count":missing_label_count,"simulation_completeness":sim_completeness,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(sim,open(C/"v11_5_paper_portfolio_simulation.json","w"),indent=2)
print(f"Simulation: {len(eligible)} portfolios, {len(results)} results, {calculated_result_count} calculated, {blocked_result_count} blocked, {missing_label_count} labels missing")
