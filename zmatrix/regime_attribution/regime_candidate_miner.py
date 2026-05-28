from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def mine_regime_candidates(*, separability: dict, regime_performance_profile: dict | None = None) -> dict:
    status = separability.get("separability_status")
    candidates = []
    if status in ("REGIME_SEPARABLE", "WEAKLY_REGIME_SEPARABLE"):
        candidates = [
            {"candidate_name":"block_b_rotation_in_bear_trend","description":"Block B_MID_ROTATION entries when market_regime is BEAR_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"entry_time_or_same_day_regime_only":True},
            {"candidate_name":"allow_b_rotation_in_bull_trend_only","description":"Allow B_MID_ROTATION only when market_regime is BULL_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"entry_time_or_same_day_regime_only":True},
            {"candidate_name":"require_non_bear_market","description":"Allow B_MID_ROTATION in BULL_TREND or RANGE_BOUND, block BEAR_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"entry_time_or_same_day_regime_only":True},
            {"candidate_name":"range_bound_observation_only","description":"Downgrade B_MID_ROTATION in RANGE_BOUND to observation-only pending secondary filter.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"entry_time_or_same_day_regime_only":True},
            {"candidate_name":"reduce_b_rotation_in_liquidity_contraction","description":"Reduce B_MID_ROTATION under LIQUIDITY_CONTRACTION.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"entry_time_or_same_day_regime_only":True},
        ]
    return {"candidate_version":"V356_REGIME_CANDIDATES_V11","source_separability_status":status,"candidate_count":len(candidates),"candidates":candidates,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
