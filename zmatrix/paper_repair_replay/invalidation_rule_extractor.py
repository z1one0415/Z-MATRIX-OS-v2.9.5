from __future__ import annotations
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def _to_loss_pct(x, default=-8.0):
    if x in (None, ""): return default
    try: v = float(x)
    except Exception: return default
    return -v if v > 0 else v

def extract_invalidation_rule(*, action: dict) -> dict:
    max_loss_plan = action.get("max_loss_plan")
    invalidation_condition = action.get("invalidation_condition")
    default_rule_used = max_loss_plan in (None, "")
    max_loss_pct = _to_loss_pct(max_loss_plan, default=-8.0)
    return {"rule_version": "V353_INVALIDATION_RULE_V10", "paper_id": action.get("paper_id"), "ticker": action.get("ticker"), "max_loss_pct": max_loss_pct, "invalidation_condition": invalidation_condition, "default_rule_used": default_rule_used, "lookahead_safe": True, "rule_available_at_entry": True, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
