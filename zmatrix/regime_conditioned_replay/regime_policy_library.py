from __future__ import annotations

REGIME_POLICIES = {
    "block_b_rotation_in_bear_trend":{"description":"Keep B_MID_ROTATION unless market_regime is BEAR_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True},
    "allow_b_rotation_in_bull_trend_only":{"description":"Keep B_MID_ROTATION only when market_regime is BULL_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True},
    "require_non_bear_market":{"description":"Keep B_MID_ROTATION in BULL_TREND or RANGE_BOUND; block BEAR_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True},
    "range_bound_observation_only":{"description":"Keep BULL_TREND entries; downgrade RANGE_BOUND to observation; block BEAR_TREND.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True},
    "reduce_b_rotation_in_liquidity_contraction":{"description":"Block or downgrade B_MID_ROTATION under LIQUIDITY_CONTRACTION.","lookahead_risk":False,"production_ready":False,"paper_replay_required":True},
}

def apply_regime_policy(*, rows: list[dict], policy_name: str) -> dict:
    policy = REGIME_POLICIES[policy_name]
    kept = []; downgraded = []
    for row in rows or []:
        regime = row.get("market_regime"); liquidity = row.get("liquidity_regime")
        action = "KEEP"
        if policy_name=="block_b_rotation_in_bear_trend":
            if regime=="BEAR_TREND": action="BLOCK"
        elif policy_name=="allow_b_rotation_in_bull_trend_only":
            if regime!="BULL_TREND": action="BLOCK"
        elif policy_name=="require_non_bear_market":
            if regime=="BEAR_TREND": action="BLOCK"
        elif policy_name=="range_bound_observation_only":
            if regime=="BEAR_TREND": action="BLOCK"
            elif regime=="RANGE_BOUND": action="OBSERVE_ONLY"
        elif policy_name=="reduce_b_rotation_in_liquidity_contraction":
            if liquidity=="LIQUIDITY_CONTRACTION": action="OBSERVE_ONLY"
        r2 = dict(row); r2["regime_policy_action"]=action; r2["policy_name"]=policy_name
        if action=="KEEP": kept.append(r2)
        else: downgraded.append(r2)
    return {"policy_name":policy_name,"policy":policy,"original_count":len(rows or []),"kept_count":len(kept),"downgraded_count":len(downgraded),"kept_rate":len(kept)/len(rows) if rows else None,"kept":kept,"downgraded":downgraded,"real_trade_allowed":False,"broker_order_allowed":False}
