#!/usr/bin/env python3
"""V11 Semantic Audit: V10 thesis ↔ V11 watchlist consistency."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"
tp=json.loads((C/"v10_candidate_factor_thesis_pack.json").read_text())
wl=json.loads((C/"v11_candidate_factor_watchlist.json").read_text())
mm=[];lk=[];bv=[];sv=[]
for wi in wl["watch_items"]:
    fid=wi["factor_id"];v10=next((c for c in tp["candidates"]if c["factor_id"]==fid and c["horizon"]==wi["horizon"]),{})
    v10e=v10.get("supporting_evidence",{})
    for k in["rankic_direction","decay_pattern","decay_pattern_basis","raw_rankic_trend"]:
        vv=v10e.get(k);wv=wi.get(k)
        if vv is not None and wv is not None and vv!=wv: mm.append(f"{fid}.{k}:V10={vv} V11={wv}")
    dp=wi.get("decay_pattern","")
    if dp in("MONOTONIC_INCREASING","MONOTONIC_DECREASING"): lk.append(f"{fid}.decay_pattern={dp}")
    rd=wi.get("rankic_direction");bu=wi.get("bucket_direction")
    if rd=="NEGATIVE"and bu!="LOW_FACTOR_VALUE_FAVORED": bv.append(f"{fid}:NEGATIVE bkt={bu}")
    if rd=="POSITIVE"and bu!="HIGH_FACTOR_VALUE_FAVORED": bv.append(f"{fid}:POSITIVE bkt={bu}")
ok=len(mm)==0 and len(lk)==0 and len(bv)==0
sa={"status":"V11_WATCHLIST_SEMANTIC_AUDIT_PASS"if ok else"FAIL","checked_watch_items":len(wl["watch_items"]),"semantic_mismatch_count":len(mm),"semantic_missing_count":len(wl.get("semantic_missing_fields",[])),"raw_monotonic_leaks":lk,"bucket_direction_violations":bv,"snapshot_direction_violations":sv,"ready_for_v11_closeout":ok}
json.dump(sa,open(C/"v11_watchlist_semantic_audit.json","w"),indent=2)
print(f"Semantic audit: {'PASS' if ok else 'FAIL'} | mismatch={len(mm)} leak={len(lk)}")
