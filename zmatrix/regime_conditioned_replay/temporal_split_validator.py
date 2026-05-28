from __future__ import annotations
from statistics import median
from zmatrix.regime_conditioned_replay.anti_overfit_schema import ANTI_OVERFIT_HURDLES

def _clean(xs):
    out=[]
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except: pass
    return out

def _year(d):
    s=str(d or "").replace("-","")
    if len(s)>=4: return s[:4]
    return s[:4] if len(s)==4 else "unknown"

def validate_temporal_stability(*, rows: list[dict], policy_names: list[str]) -> dict:
    year_groups = {}
    for r in rows or []:
        y = _year(r.get("entry_date",""))
        year_groups.setdefault(y,[]).append(r)
    years = sorted(year_groups.keys())
    if len(years) < 3: return {"temporal_status":"INSUFFICIENT_WINDOWS","window_count":len(years),"message":f"Only {len(years)} temporal windows; need >= 3"}
    results = {}
    for pn in policy_names:
        windows = []
        passes = 0
        for y in years:
            grp = year_groups[y]
            base_returns = _clean([r.get("actual_return_t20") for r in grp])
            bw = len([x for x in base_returns if x>0])/len(base_returns) if base_returns else 0
            bm = median(base_returns) if base_returns else 0
            filtered = [r for r in grp if r.get("regime_policy_action","KEEP")=="KEEP"]
            f_returns = _clean([r.get("actual_return_t20") for r in filtered])
            fw = len([x for x in f_returns if x>0])/len(f_returns) if f_returns else 0
            fm = median(f_returns) if f_returns else 0
            wd = fw-bw if fw and bw else 0
            md = fm-bm if fm is not None and bm is not None else 0
            window_pass = wd >= 0.02 and md >= 0.50
            if window_pass: passes += 1
            windows.append({"year":y,"sample_count":len(grp),"kept_count":len(filtered),"baseline_win":bw,"policy_win":fw,"win_delta":wd,"baseline_median":bm,"policy_median":fm,"median_delta":md,"pass":window_pass})
        status = "STABLE" if passes >= min(3,len(years)) else "TEMPORAL_INSTABILITY"
        results[pn] = {"temporal_status":status,"window_count":len(years),"passing_windows":passes,"windows":windows}
    return {"temporal_validation_version":"V357_TEMPORAL_VALIDATION_V10","policy_results":results}
