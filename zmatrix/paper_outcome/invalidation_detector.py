"""Invalidation Detector — check if paper trade triggered max_loss or condition"""
from __future__ import annotations

def detect_invalidation(paper_entry: dict, price_path: list[float] | None,
                         max_drawdown: float | None) -> dict:
    """Check if trade was invalidated by max_loss or condition breach."""
    if price_path is None:
        return {"invalidation_triggered": False, "reason": "insufficient_data"}
    max_loss = paper_entry.get("max_loss_plan")
    if max_loss and max_drawdown is not None and max_drawdown >= abs(float(max_loss or 0)):
        return {"invalidation_triggered": True, "reason": f"max_loss_breach:{max_drawdown}%>={max_loss}"}
    return {"invalidation_triggered": False, "reason": ""}
