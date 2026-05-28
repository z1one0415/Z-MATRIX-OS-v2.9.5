from __future__ import annotations
from statistics import median

def _clean(xs):
    out=[]
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except: pass
    return out

STRESS_REGIMES = ["BEAR_TREND","RANGE_BOUND","LIQUIDITY_CONTRACTION","HIGH_VOLATILITY"]

def validate_stress_windows(*, rows: list[dict], policy_names: list[str]) -> dict:
    results = {}
    for pn in policy_names:
        windows = []
        for sr in STRESS_REGIMES:
            grp = [r for r in rows or [] if r.get("market_regime")==sr]
            if not grp: continue
            base_returns = _clean([r.get("actual_return_t20") for r in grp])
            bw = len([x for x in base_returns if x>0])/len(base_returns) if base_returns else 0
            bm = median(base_returns) if base_returns else 0
            kept = [r for r in grp if r.get("regime_policy_action","KEEP")=="KEEP"]
            k_returns = _clean([r.get("actual_return_t20") for r in kept])
            kw = len([x for x in k_returns if x>0])/len(k_returns) if k_returns else 0
            km = median(k_returns) if k_returns else 0
            wd = kw-bw if kw and bw else 0; md = km-bm if km is not None and bm is not None else 0
            windows.append({"stress":sr,"total":len(grp),"kept":len(kept),"kept_rate":len(kept)/len(grp) if grp else 0,"baseline_win":bw,"policy_win":kw,"win_delta":wd,"baseline_median":bm,"policy_median":km,"median_delta":md,"exposure_removed":len(kept)==0})
        results[pn] = {"stress_windows":windows,"stress_status":"PASS" if all(not w.get("exposure_removed") or w.get("kept",0)>0 for w in windows) else "PASS_WITH_EXPOSURE_REMOVED"}
    return {"stress_validation_version":"V357_STRESS_VALIDATION_V10","policy_results":results}
