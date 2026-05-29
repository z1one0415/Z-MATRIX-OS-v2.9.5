# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY

def detect_beta_shakeout(*, event: dict, index_return_at_trigger: float | None = None, sector_return_at_trigger: float | None = None) -> dict:
    stock_ret = event.get("trigger_return_pct")
    if stock_ret is None: status = "BLOCKED_STOCK_TRIGGER_RETURN_MISSING"; is_beta = False
    elif index_return_at_trigger is None and sector_return_at_trigger is None: status = "BENCHMARK_UNAVAILABLE"; is_beta = False
    else:
        rel_index = (float(stock_ret) - float(index_return_at_trigger)) if index_return_at_trigger is not None else None
        rel_sector = (float(stock_ret) - float(sector_return_at_trigger)) if sector_return_at_trigger is not None else None
        is_beta = (rel_index is not None and rel_index > -3) or (rel_sector is not None and rel_sector > -3)
        status = "READY"
    return {"detector_version": "V354_BETA_SHAKEOUT_DETECTOR_V10", "detector_status": status, "paper_id": event.get("paper_id"), "ticker": event.get("ticker"), "stock_trigger_return_pct": stock_ret, "index_return_at_trigger": index_return_at_trigger, "sector_return_at_trigger": sector_return_at_trigger, "is_beta_shakeout_candidate": is_beta, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
