#!/usr/bin/env python3
"""Calculate OOS paper outcomes from resolved due labels."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
res=json.loads((C/"v11_6_1_oos_due_label_resolution.json").read_text())
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
sn=json.loads((C/"v11_paper_signal_snapshot.json").read_text())
lab_by={}
for l in lb["labels"]:lab_by[(l["as_of_date"],l["ticker"],l["horizon"])]=l
sn_map={s["watch_id"]:s for s in sn["snapshots"]}
outcomes=[];calc=0;blk=0;hit=0;mss=0
for r in res["observations"]:
    wid=r["source_watch_id"];h=r["horizon"];si=sn_map.get(wid,{})
    if r["due_label_status"]!="AVAILABLE":blk+=1;outcomes.append(dict(observation_id=r["observation_id"],factor_id=r["factor_id"],horizon=h,favored_bucket_return=None,comparison_bucket_return=None,bucket_spread=None,direction_hit=None,calculation_status="BLOCKED",blocking_reasons=["OOS_DUE_LABELS_NOT_AVAILABLE"],paper_only=True,investment_action="NONE"));continue
    ad=r["source_as_of_date"];ft=si.get("favored_bucket",[]);ct=si.get("comparison_bucket",[])
    fr=[lab_by[(ad,tk,h)]["future_relative_return"]for tk in ft if(ad,tk,h)in lab_by]
    cr=[lab_by[(ad,tk,h)]["future_relative_return"]for tk in ct if(ad,tk,h)in lab_by]
    fa=sum(fr)/len(fr)if fr else None;ca=sum(cr)/len(cr)if cr else None
    spread=fa-ca if(fa is not None and ca is not None)else None
    rd=si.get("rankic_direction","")
    dh=None
    if spread is not None:
        if rd=="NEGATIVE"and spread<0:dh=True
        elif rd=="POSITIVE"and spread>0:dh=True
        elif spread!=0:dh=False
    if dh is True:hit+=1
    elif dh is False:mss+=1
    calc+=1
    outcomes.append(dict(observation_id=r["observation_id"],factor_id=r["factor_id"],horizon=h,rankic_direction=rd,source_as_of_date=ad,favored_bucket_return=round(fa,6)if fa else None,comparison_bucket_return=round(ca,6)if ca else None,bucket_spread=round(spread,6)if spread else None,direction_hit=dh,calculation_status="CALCULATED",paper_only=True,investment_action="NONE"))
gp=sum(1 for o in outcomes if o.get("bucket_spread")and o["bucket_spread"]>0)
d=dict(status="V11_6_1_OOS_PAPER_OUTCOMES_BUILT"if calc>0 else"V11_6_1_OOS_PAPER_OUTCOMES_BLOCKED",observation_count=len(outcomes),calculated_observation_count=calc,blocked_observation_count=blk,direction_hit_count=hit,direction_miss_count=mss,direction_hit_rate=round(hit/calc,4)if calc else None,gross_positive_count=gp,ready_for_oos_completion_audit=blk==0,observations=outcomes,ready_for_alpha_claim=False,alpha_validated=False,production="BLOCKED",broker_runtime="BLOCKED",real_trade="BLOCKED")
json.dump(d,open(C/"v11_6_1_oos_paper_outcomes.json","w"),indent=2)
print(f"Outcomes: calc={calc} blocked={blk} hit={hit} miss={mss} gp={gp}")
