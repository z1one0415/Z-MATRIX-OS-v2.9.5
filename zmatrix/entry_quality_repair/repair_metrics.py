# allowlist: forbidden-token-definition
from __future__ import annotations
from statistics import median

def _clean(xs):
    out = []
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except Exception: pass
    return out

def _percentile(xs, p):
    xs = sorted(_clean(xs))
    if not xs: return None
    return xs[int(round((len(xs)-1)*p))]

def _trimmed_mean(xs, trim=0.05):
    xs = sorted(_clean(xs))
    if not xs: return None
    k = int(len(xs)*trim); ys = xs[k:len(xs)-k] if len(xs)>2*k else xs
    return sum(ys)/len(ys) if ys else None

def build_entry_repair_metrics(*, rows: list[dict], horizon: str = "t20") -> dict:
    key = f"actual_return_{horizon.lower()}"
    returns = [row.get(key) for row in rows or [] if row.get(key) is not None]
    xs = _clean(returns); wins = [x for x in xs if x>0]
    p99 = _percentile(xs, 0.99)
    top_contribution = None
    if xs and p99 is not None:
        top = [x for x in xs if x>=p99]; total_sum = sum(xs)
        top_contribution = sum(top)/total_sum if total_sum else None
    return {"metrics_version":"V355_ENTRY_REPAIR_METRICS_V10","horizon":horizon.upper(),"count":len(xs),"win_rate":len(wins)/len(xs) if xs else None,"mean":sum(xs)/len(xs) if xs else None,"median":median(xs) if xs else None,"trimmed_mean_5pct":_trimmed_mean(xs,0.05),"p25":_percentile(xs,0.25),"p75":_percentile(xs,0.75),"p95":_percentile(xs,0.95),"p99":p99,"best":max(xs) if xs else None,"worst":min(xs) if xs else None,"top_1pct_contribution":top_contribution,"real_trade_allowed":False,"broker_order_allowed":False}
