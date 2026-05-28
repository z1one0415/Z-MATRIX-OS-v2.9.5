from __future__ import annotations
from statistics import median

def _clean(xs):
    out=[]
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except: pass
    return out

def _percentile(xs,p):
    xs=sorted(_clean(xs))
    return xs[int(round((len(xs)-1)*p))] if xs else None

def _trimmed(xs,t=0.05):
    xs=sorted(_clean(xs))
    if not xs: return None
    k=int(len(xs)*t); ys=xs[k:len(xs)-k] if len(xs)>2*k else xs
    return sum(ys)/len(ys) if ys else None

def build_replay_metrics(*, rows: list[dict], horizon: str = "t20") -> dict:
    k=f"actual_return_{horizon.lower()}"
    returns=[r.get(k) for r in rows or [] if r.get(k) is not None]
    xs=_clean(returns); wins=[x for x in xs if x>0]
    inv=[r.get("invalidation_triggered") for r in rows or []]
    inv_r=sum(1 for x in inv if x is True)/len(inv) if inv else None
    p99=_percentile(xs,0.99)
    top_c=None
    if xs and p99 is not None:
        t=[x for x in xs if x>=p99]; ts=sum(xs)
        top_c=sum(t)/ts if ts else None
    return {"count":len(xs),"win_rate":len(wins)/len(xs) if xs else None,"mean":sum(xs)/len(xs) if xs else None,"median":median(xs) if xs else None,"trimmed_mean_5pct":_trimmed(xs,0.05),"p25":_percentile(xs,0.25),"p75":_percentile(xs,0.75),"p95":_percentile(xs,0.95),"p99":p99,"best":max(xs) if xs else None,"worst":min(xs) if xs else None,"invalidation_rate":inv_r,"top_1pct_contribution":top_c}
