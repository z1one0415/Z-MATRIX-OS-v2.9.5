from __future__ import annotations
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def simulate_invalidation_exit(*, action: dict, price_path: dict, rule: dict, horizon_days: int = 20) -> dict:
    bars = price_path.get("bars", [])
    if not bars:
        return {"simulation_status": "BLOCKED_PRICE_PATH_MISSING", "paper_id": action.get("paper_id"), "ticker": action.get("ticker"), "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
    entry_price = action.get("entry_price")
    if entry_price in (None, ""): entry_price = bars[0]["close"]
    entry_price = float(entry_price)
    max_loss_pct = float(rule.get("max_loss_pct", -8.0))
    exit_triggered = False; exit_bar = None; daily_trace = []
    for i, bar in enumerate(bars[:horizon_days]):
        close = float(bar["close"]); ret = (close - entry_price) / entry_price * 100
        daily_trace.append({"idx": i, "trade_date": bar["trade_date"], "close": close, "return_pct": round(ret, 4)})
        if ret <= max_loss_pct: exit_triggered = True; exit_bar = bar; break
    if exit_triggered:
        exit_price = float(exit_bar["close"]); exit_date = exit_bar["trade_date"]; exit_reason = "INVALIDATION_EXIT_TRIGGERED"
    else:
        idx = min(horizon_days, len(bars)) - 1; exit_price = float(bars[idx]["close"]); exit_date = bars[idx]["trade_date"]; exit_reason = "HORIZON_EXIT"
    repaired_return = (exit_price - entry_price) / entry_price * 100
    return {"simulation_version": "V353_INVALIDATION_EXIT_SIMULATION_V10", "simulation_status": "READY", "paper_id": action.get("paper_id"), "ticker": action.get("ticker"), "role": action.get("role"), "entry_date": action.get("entry_date"), "entry_price": entry_price, "exit_triggered": exit_triggered, "exit_date": exit_date, "exit_price": exit_price, "exit_reason": exit_reason, "max_loss_pct": max_loss_pct, "repaired_return": round(repaired_return, 4), "daily_trace_sample": daily_trace[:10], "lookahead_safe": True, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY)}
