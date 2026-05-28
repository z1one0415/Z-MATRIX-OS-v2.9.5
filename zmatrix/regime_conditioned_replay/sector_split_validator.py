from __future__ import annotations
from statistics import median

def _clean(xs):
    out=[]
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except: pass
    return out

def validate_sector_stability(*, rows: list[dict], policy_names: list[str]) -> dict:
    sector_map = {}
    for r in rows or []:
        sc = r.get("sector") or r.get("industry") or r.get("sector_code") or (r.get("source_brd_result",{}) or {}).get("sector")
        if not sc: sc = "UNKNOWN"
        sector_map.setdefault(sc,[]).append(r)
    if not sector_map or list(sector_map.keys())==["UNKNOWN"]: return {"sector_status":"DATA_INSUFFICIENT","sector_group_count":0,"message":"No sector data available"}
    results = {}
    for pn in policy_names:
        groups = []
        passes = 0
        for s, grp in sector_map.items():
            if len(grp) < 100: continue
            base_returns = _clean([r.get("actual_return_t20") for r in grp])
            bw = len([x for x in base_returns if x>0])/len(base_returns) if base_returns else 0
            bm = median(base_returns) if base_returns else 0
            filtered = [r for r in grp if r.get("regime_policy_action","KEEP")=="KEEP"]
            f_returns = _clean([r.get("actual_return_t20") for r in filtered])
            fw = len([x for x in f_returns if x>0])/len(f_returns) if f_returns else 0
            fm = median(f_returns) if f_returns else 0
            wd = fw-bw if fw and bw else 0; md = fm-bm if fm is not None and bm is not None else 0
            if wd >= 0.02 and md >= 0.50: passes += 1
            groups.append({"sector":s,"count":len(grp),"kept":len(filtered),"baseline_win":bw,"policy_win":fw,"win_delta":wd,"baseline_median":bm,"policy_median":fm,"median_delta":md,"pass":wd>=0.02 and md>=0.50})
        status = "STABLE" if passes >= min(3,len(groups)) else "SECTOR_INSTABILITY"
        results[pn] = {"sector_status":status,"sector_group_count":len(groups),"passing_groups":passes,"groups":groups}
    return {"sector_validation_version":"V357_SECTOR_VALIDATION_V10","policy_results":results}
