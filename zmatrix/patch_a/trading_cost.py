"""PATCH-A-5: Trading Cost + Tradability Model"""
from __future__ import annotations

TRADING_COST_DEFAULTS = {"commission_rate":0.0003,"stamp_tax_rate":0.001,"min_commission":5.0,"slippage_bps":5,"limit_board_impact_bps":50,"suspension_cost_pct":0,"capacity_threshold_pct":0.03}

def compute_net_return(*, gross_return_pct: float, entry_price: float, exit_price: float, volume: float, market_cap: float | None = None, limit_board_flags: dict | None = None) -> dict:
    lb = limit_board_flags or {}
    # Commission + stamp tax
    entry_commission = max(TRADING_COST_DEFAULTS["min_commission"], entry_price * volume * TRADING_COST_DEFAULTS["commission_rate"])
    exit_commission = max(TRADING_COST_DEFAULTS["min_commission"], exit_price * volume * TRADING_COST_DEFAULTS["commission_rate"])
    stamp_tax = exit_price * volume * TRADING_COST_DEFAULTS["stamp_tax_rate"]
    total_cost = entry_commission + exit_commission + stamp_tax
    notional = entry_price * volume
    cost_pct = total_cost / notional * 100 if notional else 0
    # Slippage
    slippage_pct = TRADING_COST_DEFAULTS["slippage_bps"] / 100
    # Limit board
    limit_penalty = 0; execution_feasible = True; limit_reasons = []
    if lb.get("limit_up_flag") and lb.get("one_price_board_flag"): limit_penalty += TRADING_COST_DEFAULTS["limit_board_impact_bps"] / 100; execution_feasible = False; limit_reasons.append("ONE_PRICE_BOARD_BUY_BLOCKED")
    if lb.get("limit_down_flag"): execution_feasible = False; limit_reasons.append("LIMIT_DOWN_SELL_BLOCKED")
    if lb.get("suspension_flag"): execution_feasible = False; limit_reasons.append("SUSPENSION")
    # Capacity check
    capacity_ok = True
    if market_cap and volume * entry_price / market_cap > TRADING_COST_DEFAULTS["capacity_threshold_pct"]: capacity_ok = False; limit_reasons.append("CAPACITY_EXCEEDED")
    net_return = gross_return_pct - cost_pct - slippage_pct - limit_penalty
    return {"gross_return_pct": gross_return_pct, "net_return_pct": net_return, "cost_pct": cost_pct, "slippage_pct": slippage_pct, "limit_penalty_pct": limit_penalty, "execution_feasible": execution_feasible and capacity_ok, "limit_reasons": limit_reasons, "liquidity_capacity_status": "ADEQUATE" if capacity_ok else "INSUFFICIENT"}
