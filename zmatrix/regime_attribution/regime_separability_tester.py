# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY, DEFAULT_REGIME_THRESHOLDS

def _sf(x,d=None):
    try:
        if x is None: return d
        return float(x)
    except: return d

def _clip01(x): return max(0.0,min(1.0,float(x)))

def _distribution_score(rows):
    good=[r for r in rows or [] if _sf(r.get("actual_return_t20"),0)>0 and not r.get("invalidation_triggered")]
    bad=[r for r in rows or [] if _sf(r.get("actual_return_t20"),0)<0 or r.get("invalidation_triggered")]
    if len(good)<1000 or len(bad)<1000: return {"status":"DATA_INSUFFICIENT","score":0,"good_count":len(good),"bad_count":len(bad)}
    def dist(rs):
        d={}
        for r in rs: mr=r.get("market_regime","UNKNOWN_MARKET_REGIME"); d[mr]=d.get(mr,0)+1
        t=len(rs); return {k:v/t for k,v in d.items()} if t else {}
    gd=dist(good); bd=dist(bad); all_r=set(list(gd.keys())+list(bd.keys()))
    return {"status":"READY","score":sum(abs(gd.get(r,0)-bd.get(r,0)) for r in all_r)/2,"good_count":len(good),"bad_count":len(bad),"good_distribution":gd,"bad_distribution":bd}

def _get_profiles(p): return (p or {}).get("market_regime_profiles") or (p or {}).get("profiles") or {}

def _bull_bear_spread(profile):
    p=_get_profiles(profile); bull=p.get("BULL_TREND"); bear=p.get("BEAR_TREND")
    if not bull or not bear: return {"status":"MISSING_BULL_OR_BEAR","bull_count":0,"bear_count":0}
    bc=int(bull.get("count")or 0); ec=int(bear.get("count")or 0)
    bw=_sf(bull.get("win_rate")); ew=_sf(bear.get("win_rate"))
    bm=_sf(bull.get("median")); em=_sf(bear.get("median"))
    bi=_sf(bull.get("invalidation_rate")); ei=_sf(bear.get("invalidation_rate"))
    return {"status":"READY","bull_count":bc,"bear_count":ec,"bull":bull,"bear":bear,"win_rate_spread":(bw-ew) if bw is not None and ew is not None else None,"median_spread":(bm-em) if bm is not None and em is not None else None,"invalidation_spread":(ei-bi) if ei is not None and bi is not None else None}

def _spread_scores(s):
    return {"win_rate_spread_score":_clip01(_sf(s.get("win_rate_spread"),0)/0.15),"median_spread_score":_clip01(_sf(s.get("median_spread"),0)/3.0),"invalidation_spread_score":_clip01(_sf(s.get("invalidation_spread"),0)/0.25)}

def _sample_balance_score(s,ms):
    b=int(s.get("bull_count")or 0); e=int(s.get("bear_count")or 0)
    return _clip01(min(b,e)/max(1,ms)) if b>0 and e>0 else 0

def _override(s,th):
    if s.get("status")!="READY": return None
    if s.get("bull_count",0)<th["bull_bear_min_sample"] or s.get("bear_count",0)<th["bull_bear_min_sample"]: return None
    if (_sf(s.get("win_rate_spread"),0)>=th["bull_bear_win_rate_spread"] and _sf(s.get("median_spread"),0)>=th["bull_bear_median_spread"] and _sf(s.get("invalidation_spread"),0)>=th["bull_bear_invalidation_spread"]): return "WEAKLY_REGIME_SEPARABLE"
    return None

def test_regime_separability(*, enriched_rows: list[dict], regime_performance_profile: dict | None = None) -> dict:
    th=DEFAULT_REGIME_THRESHOLDS; perf=regime_performance_profile or {}
    dist=_distribution_score(enriched_rows); spread=_bull_bear_spread(perf)
    ss=_spread_scores(spread); bal=_sample_balance_score(spread,th["bull_bear_min_sample"])
    ds=_sf(dist.get("score"),0); ws=ss["win_rate_spread_score"]; ms=ss["median_spread_score"]; invs=ss["invalidation_spread_score"]
    sep_score=ds*0.20+ws*0.25+ms*0.25+invs*0.20+bal*0.10
    over=_override(spread,th)
    if dist.get("status")=="DATA_INSUFFICIENT" and spread.get("status")!="READY": status="DATA_INSUFFICIENT"
    elif sep_score>=th["regime_separable_score"]: status="REGIME_SEPARABLE"
    elif sep_score>=th["weakly_regime_separable_score"]: status="WEAKLY_REGIME_SEPARABLE"
    elif over: status=over
    else: status="NOT_REGIME_SEPARABLE"
    return {"separability_version":"V356_REGIME_SEPARABILITY_V11","separability_status":status,"separability_score":sep_score,"scoring_breakdown":{"distribution_score":ds,"win_rate_spread_score":ws,"median_spread_score":ms,"invalidation_spread_score":invs,"sample_balance_score":bal,"composite_weights":{"distribution":0.20,"win_rate":0.25,"median":0.25,"invalidation":0.20,"balance":0.10}},"bull_bear_spread":spread,"good_bad_distribution":{"good_count":dist.get("good_count"),"bad_count":dist.get("bad_count"),"good_distribution":dist.get("good_distribution"),"bad_distribution":dist.get("bad_distribution")},"top_discriminating_regime_features":[{"feature":"market_regime","evidence":"BULL vs BEAR spread","win_rate_spread":spread.get("win_rate_spread"),"median_spread":spread.get("median_spread"),"invalidation_spread":spread.get("invalidation_spread"),"score":max(ws,ms,invs)},{"feature":"index_trend_state","evidence":"proxied by BULL/BEAR","score":ws},{"feature":"index_above_ma60","evidence":"implicit in regime builder","score":ms},{"feature":"index_return_20d","evidence":"implicit","score":ws},{"feature":"index_volatility","evidence":"implicit","score":invs}],"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
