# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY

def _to_float(x):
    try:
        if x in (None, ""): return None
        return float(x)
    except Exception: return None

def build_trigger_day_features(*, event: dict, price_bars: list[dict]) -> dict:
    if event.get("event_status") != "READY": return {"feature_status": "BLOCKED_EVENT_NOT_READY", "features": {}, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    idx = int(event.get("trigger_idx", 0))
    if idx >= len(price_bars): return {"feature_status": "BLOCKED_TRIGGER_BAR_MISSING", "features": {}, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    bar = price_bars[idx]
    open_p = _to_float(bar.get("open")); high = _to_float(bar.get("high")); low = _to_float(bar.get("low")); close = _to_float(bar.get("close")); vol = _to_float(bar.get("volume") or bar.get("vol"))
    ohlc_ready = all(x is not None for x in (open_p, high, low, close)) and high != low
    clv = (close - low) / (high - low) if ohlc_ready else None
    upper_shadow_pct = (high - max(open_p, close)) / close * 100 if ohlc_ready and close else None
    lower_shadow_pct = (min(open_p, close) - low) / close * 100 if ohlc_ready and close else None
    intraday_return_pct = (close - open_p) / open_p * 100 if ohlc_ready and open_p else None
    features = {"trigger_date": bar.get("trade_date"), "trigger_close": close, "trigger_volume": vol, "ohlc_ready": ohlc_ready, "trigger_day_clv": clv, "upper_shadow_pct": upper_shadow_pct, "lower_shadow_pct": lower_shadow_pct, "intraday_return_pct": intraday_return_pct, "trigger_return_pct": event.get("trigger_return_pct")}
    return {"feature_version": "V354_TRIGGER_DAY_FEATURES_V10", "feature_status": "READY", "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "features": features, "uses_future_data": False, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
