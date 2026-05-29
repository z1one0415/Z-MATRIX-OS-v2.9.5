# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY

def _to_float(x):
    try:
        if x in (None, ""): return None
        return float(x)
    except Exception: return None

def build_recovery_profile(*, event: dict, price_bars: list[dict]) -> dict:
    if event.get("event_status") != "READY": return {"profile_status": "BLOCKED_EVENT_NOT_READY", "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    entry_price = _to_float(event.get("entry_price"))
    trigger_idx = int(event.get("trigger_idx", 0))
    if entry_price is None: return {"profile_status": "BLOCKED_ENTRY_PRICE_MISSING", "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    result = {"profile_version": "V354_RECOVERY_PROFILE_V10", "profile_status": "READY", "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "label_used_for_analysis_only": True, "must_not_use_as_live_decision": True, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    for h in [1, 2, 3, 5, 20]:
        idx = trigger_idx + h
        if idx >= len(price_bars): result[f"rebound_after_trigger_{h}d"] = None; continue
        close = _to_float(price_bars[idx].get("close"))
        result[f"rebound_after_trigger_{h}d"] = (close - entry_price) / entry_price * 100 if close is not None else None
    return result
