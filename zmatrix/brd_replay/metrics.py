"""Strategy Metrics — win rate, avg return, invalidated rate"""
from __future__ import annotations
def _valid(xs): return [float(x) for x in xs if x is not None]
def _mean(xs): return sum(xs)/len(xs) if xs else None

def build_strategy_metrics(*, outcomes, horizon="t20"):
    ret_key = f"actual_return_{horizon.lower()}"
    returns = _valid([x.get(ret_key) for x in outcomes])
    wins = [x for x in returns if x>0]
    invalidated = [x for x in outcomes if x.get("invalidation_triggered") is True]
    ready = [x for x in outcomes if x.get("outcome_status")=="READY"]
    return {"metrics_version":"BRD_STRATEGY_METRICS_V10","horizon":horizon.upper(),
            "sample_count":len(outcomes),"ready_count":len(ready),"valid_return_count":len(returns),
            "win_count":len(wins),"win_rate":len(wins)/len(returns) if returns else None,
            "average_return":_mean(returns),"invalidated_count":len(invalidated),
            "invalidated_rate":len(invalidated)/len(outcomes) if outcomes else None,
            "real_trade_allowed":False,"broker_order_allowed":False}
