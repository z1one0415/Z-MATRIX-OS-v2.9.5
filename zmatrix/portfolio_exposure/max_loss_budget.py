"""Max Loss Budget — aggregate max_loss_plan across positions"""
from __future__ import annotations

def calc_max_loss_budget(positions: list[dict]) -> dict:
    """Calculate total max loss budget across positions."""
    budgets = []
    total = 0.0
    for p in positions:
        ml = float(p.get("max_loss_plan", 0) or 0)
        w = float(p.get("weight", 0) or 0)
        if ml > 0 and w > 0:
            loss = w * ml
            budgets.append({"ticker": p.get("ticker"), "max_loss": ml, "weighted_loss": round(loss, 4)})
            total += loss
    return {
        "total_max_loss_budget": round(total, 4),
        "position_budgets": budgets,
        "real_trade_allowed": False, "broker_order_allowed": False,
    }
