# allowlist: forbidden-token-definition
from __future__ import annotations
from statistics import median
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def _clean(xs):
    out = []
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except: pass
    return out

def _stats(returns, invals):
    xs = _clean(returns); wins = [x for x in xs if x>0]
    inv = sum(1 for x in invals if x is True)
    p99 = sorted(xs)[int(round((len(xs)-1)*0.99))] if xs else None
    top_cont = sum(x for x in xs if p99 and x>=p99)/sum(xs) if xs and p99 and sum(xs) else None
    return {"count":len(xs),"win_rate":len(wins)/len(xs) if xs else None,"mean":sum(xs)/len(xs) if xs else None,"median":median(xs) if xs else None,"trimmed":sum(sorted(xs)[int(len(xs)*0.05):len(xs)-int(len(xs)*0.05)])/max(1,len(xs)-2*int(len(xs)*0.05)) if len(xs)>10 else None,"invalidation_rate":inv/len(invals) if invals else None,"top_1pct_contribution":top_cont}

def profile_regime_performance(*, enriched_rows: list[dict]) -> dict:
    dims = {}
    for r in enriched_rows or []:
        mr = r.get("market_regime","UNKNOWN_MARKET_REGIME")
        dims.setdefault(mr,[]).append(r)
    profiles = {}
    for mr, rows in dims.items():
        rets = [r.get("actual_return_t20") for r in rows]
        invs = [r.get("invalidation_triggered") for r in rows]
        profiles[mr] = _stats(rets, invs)
    sorted_profiles = sorted(profiles.items(), key=lambda x: x[1].get("median") or -99, reverse=True)
    best = sorted_profiles[0] if sorted_profiles else (None,None)
    worst = sorted_profiles[-1] if sorted_profiles else (None,None)
    return {"profile_version":"V356_REGIME_PERFORMANCE_V10","market_regime_profiles":dict(sorted_profiles),"best_regime_segment":{"regime":best[0],"stats":best[1]} if best[0] else None,"worst_regime_segment":{"regime":worst[0],"stats":worst[1]} if worst[0] else None,"market_regime_counts":{k:len(v) for k,v in dims.items()},"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
