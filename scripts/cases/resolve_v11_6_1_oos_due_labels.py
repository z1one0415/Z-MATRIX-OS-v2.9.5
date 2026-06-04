#!/usr/bin/env python3
"""Resolve OOS due labels from forward label data."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases";L=W/"runtime_reports/cases/v8_large_data"
lb=json.loads((L/"v8_forward_return_labels.json").read_text())
sn=json.loads((C/"v11_paper_signal_snapshot.json").read_text())
reg=json.loads((C/"v11_6_tracking_registry.json").read_text())
lab_by={}
for l in lb["labels"]:lab_by[(l["as_of_date"],l["ticker"],l["horizon"])]=l
ad=sn["as_of_date"];sn_map={s["watch_id"]:s for s in sn["snapshots"]}
resolved=[];avail=0;partial=0;missing=0
for obs in reg["observations"]:
    wid=obs["source_watch_id"];h=obs["horizon"];si=sn_map.get(wid,{})
    ft=si.get("favored_bucket",[]);ct=si.get("comparison_bucket",[])
    ff=sum(1 for tk in ft if(ad,tk,h)in lab_by);cf=sum(1 for tk in ct if(ad,tk,h)in lab_by)
    fm=len(ft)-ff;cm=len(ct)-cf;tm=fm+cm
    st="AVAILABLE"if tm==0 else("PARTIAL"if ff+cf>0 else"MISSING")
    if st=="AVAILABLE":avail+=1
    elif st=="PARTIAL":partial+=1
    else:missing+=1
    resolved.append(dict(observation_id=obs["observation_id"],source_watch_id=wid,factor_id=obs["factor_id"],source_as_of_date=ad,horizon=h,favored_labels_required=len(ft),comparison_labels_required=len(ct),favored_labels_found=ff,comparison_labels_found=cf,missing_favored_labels=fm,missing_comparison_labels=cm,due_label_status=st,paper_only=True,investment_action="NONE"))
all_avail=avail==reg["observation_count"]
r=dict(status="V11_6_1_OOS_DUE_LABEL_RESOLUTION_BUILT",observation_count=len(resolved),available_observation_count=avail,partial_observation_count=partial,missing_observation_count=missing,all_due_labels_available=all_avail,ready_for_completion=all_avail,blocking_reasons=[]if all_avail else["OOS_DUE_LABELS_NOT_AVAILABLE"],observations=resolved)
json.dump(r,open(C/"v11_6_1_oos_due_label_resolution.json","w"),indent=2)
print(f"Due Labels: avail={avail}/{len(resolved)} partial={partial} missing={missing}")
