from __future__ import annotations
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY, DEFAULT_ANATOMY_THRESHOLDS

def _to_float(x):
    try:
        if x in (None, ""): return None
        return float(x)
    except Exception: return None

def label_post_invalidation_path(*, event: dict, price_bars: list[dict], thresholds: dict | None = None) -> dict:
    th = dict(DEFAULT_ANATOMY_THRESHOLDS)
    if thresholds: th.update(thresholds)
    if event.get("event_status") != "READY": return {"label_status": "BLOCKED_EVENT_NOT_READY", "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    entry_price = _to_float(event.get("entry_price"))
    trigger_idx = int(event.get("trigger_idx", 0))
    post = price_bars[trigger_idx:]
    if not post or entry_price is None: return {"label_status": "BLOCKED_POST_PATH_MISSING", "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    returns = []
    for i, bar in enumerate(post[:20]):
        close = _to_float(bar.get("close"))
        if close is None: continue
        ret = (close - entry_price) / entry_price * 100
        returns.append({"post_idx": i, "trade_date": bar.get("trade_date"), "return_pct": ret, "close": close})
    if not returns: path_type = "UNKNOWN_PATH"
    else:
        max_ret_5 = max([x["return_pct"] for x in returns[:5]]) if len(returns) >= 1 else None
        max_ret_20 = max([x["return_pct"] for x in returns])
        final_ret_20 = returns[min(len(returns), 20) - 1]["return_pct"]
        if max_ret_5 is not None and max_ret_5 >= th["fast_recovery_level_pct"]: path_type = "FAST_RECOVERY"
        elif final_ret_20 >= th["slow_recovery_level_pct"]: path_type = "SLOW_RECOVERY"
        elif final_ret_20 <= th["true_breakdown_t20_pct"]: path_type = "TRUE_BREAKDOWN"
        elif max_ret_20 >= th["high_vol_winner_t20_pct"]: path_type = "HIGH_VOLATILITY_WINNER"
        else: path_type = "UNKNOWN_PATH"
    return {"label_version": "V354_POST_INVALIDATION_PATH_LABEL_V10", "label_status": "READY", "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "path_type": path_type, "post_trigger_returns_sample": returns[:10], "label_used_for_analysis_only": True, "must_not_use_as_entry_filter": True, "must_not_use_as_live_decision": True, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
