"""ResearchDB Account Truth — drawdown calculator."""
from __future__ import annotations


def calculate_drawdowns(curve: list[dict]) -> list[dict]:
    """Identify drawdown periods from a capital curve."""
    if not curve:
        return []
    drawdowns = []
    peak = curve[0].get("total_equity", 0)
    in_dd = False
    dd_start = None
    dd_trough = None
    dd_trough_val = float("inf")
    
    for point in curve:
        equity = float(point.get("total_equity", 0))
        date = point.get("date", "")
        if equity >= peak:
            if in_dd and dd_start:
                drawdowns.append({
                    "start_date": dd_start,
                    "trough_date": dd_trough,
                    "end_date": date,
                    "drawdown_pct": (dd_trough_val - peak) / peak if peak > 0 else 0,
                    "duration_days": 0,
                    "recovery_days": 0,
                    "related_positions": "",
                    "quality_status": "READY",
                })
            peak = equity
            in_dd = False
        else:
            if not in_dd:
                dd_start = date
                in_dd = True
            if equity < dd_trough_val:
                dd_trough_val = equity
                dd_trough = date
    
    return drawdowns
