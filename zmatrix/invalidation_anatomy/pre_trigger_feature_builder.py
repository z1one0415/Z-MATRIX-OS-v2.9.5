from __future__ import annotations
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY

def _to_float(x):
    try:
        if x in (None, ""): return None
        return float(x)
    except Exception: return None

def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None

def build_pre_trigger_features(*, event: dict, price_bars: list[dict]) -> dict:
    if event.get("event_status") != "READY": return {"feature_status": "BLOCKED_EVENT_NOT_READY", "features": {}, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    trigger_idx = int(event.get("trigger_idx", 0))
    entry_price = _to_float(event.get("entry_price"))
    pre = price_bars[:max(trigger_idx, 1)]
    closes = [_to_float(x.get("close")) for x in pre]; closes = [x for x in closes if x is not None]
    vols = [_to_float(x.get("volume") or x.get("vol")) for x in pre]; vols = [x for x in vols if x is not None]
    if not closes or entry_price is None: return {"feature_status": "INSUFFICIENT_PRE_TRIGGER_DATA", "features": {}, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    last = closes[-1]; pre_return = (last - entry_price) / entry_price * 100
    features = {"time_to_invalidation": trigger_idx, "pre_trigger_return_pct": pre_return, "drawdown_speed": pre_return / max(trigger_idx, 1), "pre_trigger_volume_avg": _mean(vols), "pre_trigger_price_min": min(closes), "pre_trigger_price_max": max(closes)}
    return {"feature_version": "V354_PRE_TRIGGER_FEATURES_V10", "feature_status": "READY", "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "features": features, "uses_future_data": False, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
