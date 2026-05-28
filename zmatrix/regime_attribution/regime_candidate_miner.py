from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def mine_regime_candidates(*, separability: dict) -> dict:
    status = separability.get("separability_status")
    candidates = []
    if status in ("REGIME_SEPARABLE","WEAKLY_REGIME_SEPARABLE"):
        candidates.append({"candidate_name":"filter_bear_trend_entries","description":"Exclude B_MID_ROTATION entries when market is BEAR_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"entry_time_or_same_day_regime_only":True})
    return {"candidate_version":"V356_REGIME_CANDIDATES_V10","source_separability_status":status,"candidate_count":len(candidates),"candidates":candidates,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
