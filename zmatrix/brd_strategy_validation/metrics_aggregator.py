"""Metrics Aggregator — compute T5/T20/T60 stats from all outcomes"""
from __future__ import annotations

def _tof(x,d=None):
    try: return float(x) if x is not None else d
    except: return d

def _mean(xs):
    xs=[x for x in xs if x is not None]
    return sum(xs)/len(xs) if xs else None

def _median(xs):
    xs=sorted([x for x in xs if x is not None])
    return xs[len(xs)//2] if xs else None

def _metric_for_horizon(outcomes, horizon):
    key = f"actual_return_{horizon.lower()}"
    returns = [_tof(o.get(key)) for o in outcomes]
    returns = [x for x in returns if x is not None]
    wins=[x for x in returns if x>0]
    losses=[x for x in returns if x<=0]
    mae=[_tof(o.get("max_adverse_excursion_pct")) for o in outcomes]
    mae=[x for x in mae if x is not None]
    invalidated=[o for o in outcomes if o.get("invalidation_triggered") is True]
    ready=[o for o in outcomes if o.get("outcome_status")=="READY"]
    return {"horizon":horizon.upper(),"sample_count":len(outcomes),"ready_count":len(ready),
            "valid_return_count":len(returns),"win_count":len(wins),"loss_count":len(losses),
            "win_rate":len(wins)/len(returns) if returns else None,
            "average_return":_mean(returns),"median_return":_median(returns),
            "best_return":max(returns) if returns else None,"worst_return":min(returns) if returns else None,
            "average_mae":_mean(mae),"worst_mae":min(mae) if mae else None,
            "invalidated_count":len(invalidated),
            "invalidated_rate":len(invalidated)/len(outcomes) if outcomes else None}

def aggregate_validation_metrics(*, replay_result, horizon="t20"):
    actions, outcomes = [], []
    for daily in replay_result.get("daily_results",[]):
        actions.extend(daily.get("paper_actions",[]))
        outcomes.extend(daily.get("outcomes",[]))
    no_action=[a for a in actions if a.get("paper_action") in ("NO_ACTION","DATA_GAP")]
    active=[a for a in actions if a.get("paper_action") not in ("NO_ACTION","DATA_GAP")]
    return {"metrics_version":"V35_VALIDATION_METRICS_V10","total_paper_actions":len(actions),
            "active_paper_actions":len(active),"no_action_count":len(no_action),
            "no_action_rate":len(no_action)/len(actions) if actions else None,
            "total_outcomes":len(outcomes),
            "valid_outcome_count":sum(1 for o in outcomes if o.get("outcome_status")=="READY"),
            "t5":_metric_for_horizon(outcomes,"t5"),"t20":_metric_for_horizon(outcomes,"t20"),
            "t60":_metric_for_horizon(outcomes,"t60"),"primary":_metric_for_horizon(outcomes,horizon),
            "real_trade_allowed":False,"broker_order_allowed":False}
