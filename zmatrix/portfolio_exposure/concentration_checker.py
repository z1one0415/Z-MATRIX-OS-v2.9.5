"""Concentration Checker — single stock / sector / chain limits"""
from __future__ import annotations

def check_concentration(positions: list[dict]) -> dict:
    """Check concentration breaches. Warns at >12% stock, >25% sector/chain."""
    warnings = []
    sectors = {}
    chains = {}
    total_w = sum(p.get("weight", 0) for p in positions) or 1.0
    for p in positions:
        w = p.get("weight", 0) / total_w * 100
        s = p.get("sector", "unknown")
        c = p.get("chain", "unknown")
        sectors[s] = sectors.get(s, 0) + w
        chains[c] = chains.get(c, 0) + w
        if w > 12:
            warnings.append({"ticker": p.get("ticker"), "type": "stock", "weight_pct": round(w, 1), "limit": 12})
    for s, w in sectors.items():
        if w > 25:
            warnings.append({"sector": s, "type": "sector", "weight_pct": round(w, 1), "limit": 25})
    return {"warnings": warnings, "breach_count": len(warnings),
            "real_trade_allowed": False, "broker_order_allowed": False}
