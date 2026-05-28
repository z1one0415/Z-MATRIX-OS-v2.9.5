from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY, DEFAULT_REGIME_THRESHOLDS

def test_regime_separability(*, enriched_rows: list[dict]) -> dict:
    good = [r for r in enriched_rows or [] if r.get("actual_return_t20",0)>0 and not r.get("invalidation_triggered")]
    bad = [r for r in enriched_rows or [] if r.get("actual_return_t20",0)<0 or r.get("invalidation_triggered")]
    if len(good)<1000 or len(bad)<1000: return {"separability_status":"DATA_INSUFFICIENT","separability_score":0,"good_count":len(good),"bad_count":len(bad),"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
    def regime_dist(rows):
        d = {}
        for r in rows:
            mr = r.get("market_regime","UNKNOWN_MARKET_REGIME"); d[mr]=d.get(mr,0)+1
        total = len(rows)
        return {k:v/total for k,v in d.items()} if total else {}
    gd = regime_dist(good); bd = regime_dist(bad)
    all_regimes = set(list(gd.keys())+list(bd.keys()))
    separability_score = sum(abs(gd.get(r,0)-bd.get(r,0)) for r in all_regimes)/2 if all_regimes else 0
    th = DEFAULT_REGIME_THRESHOLDS
    if separability_score >= th["regime_separable_score"]: status = "REGIME_SEPARABLE"
    elif separability_score >= th["weakly_regime_separable_score"]: status = "WEAKLY_REGIME_SEPARABLE"
    else: status = "NOT_REGIME_SEPARABLE"
    return {"separability_version":"V356_REGIME_SEPARABILITY_V10","separability_status":status,"separability_score":separability_score,"good_distribution":gd,"bad_distribution":bd,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
