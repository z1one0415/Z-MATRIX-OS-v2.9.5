# allowlist: forbidden-token-definition
from __future__ import annotations
from statistics import median
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def _f(x):
    try:
        if x is None: return None
        return float(x)
    except: return None

def _trim(vals,t):
    if not vals: return None
    k=int(len(vals)*t); ys=vals[k:len(vals)-k] if len(vals)>2*k else vals
    return sum(ys)/len(ys) if ys else None

def _top1(vals):
    if not vals: return None
    total=sum(vals)
    if total==0: return None
    return sum(vals[-max(1,int(len(vals)*0.01)):])/total

def _stats(rows):
    vals=[]; inv=0
    for r in rows:
        v=_f(r.get("actual_return_t20"))
        if v is not None: vals.append(v)
        if r.get("invalidation_triggered") or r.get("baseline_invalidation_triggered"): inv+=1
    sv=sorted(vals); wins=[x for x in vals if x>0]
    return {"count":len(vals),"win_rate":len(wins)/len(vals) if vals else None,"mean":sum(vals)/len(vals) if vals else None,"median":median(vals) if vals else None,"trimmed_mean_5pct":_trim(sv,0.05),"invalidation_rate":inv/len(rows) if rows else None,"best":max(vals) if vals else None,"worst":min(vals) if vals else None,"top_1pct_contribution":_top1(sv)}

def profile_joint_segments(*, joined_rows: list[dict]) -> dict:
    specs = {"market_regime":["market_regime"],"sector_phase":["sector_phase"],"market_regime_x_sector_phase":["market_regime","sector_phase"],"market_regime_x_sector":["market_regime","sector"],"sector_x_sector_phase":["sector","sector_phase"]}
    profiles = {}
    for name,keys in specs.items():
        buckets = {}
        for r in joined_rows or []:
            key = tuple(r.get(k,"UNKNOWN") for k in keys)
            buckets.setdefault(key,[]).append(r)
        profiles[name] = {"|".join(map(str,k)):_stats(rs) for k,rs in buckets.items()}
    return {"profiler_version":"V3512_JOINT_SEGMENT_PROFILER_V10","profiles":profiles,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
