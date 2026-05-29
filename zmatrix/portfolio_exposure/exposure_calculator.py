# allowlist: forbidden-token-definition
"""Exposure Calculator — sector/chain/concentration analysis"""
from __future__ import annotations


def calc_exposure(positions: list[dict]) -> dict:
    """Calculate sector and chain concentration from positions."""
    sectors = {}
    chains = {}
    total_weight = sum(p.get("weight", 0) for p in positions) or 1.0
    warnings = []
    for p in positions:
        w = p.get("weight", 0)
        s = p.get("sector", "unknown")
        c = p.get("chain", "unknown")
        sectors[s] = sectors.get(s, 0) + w
        chains[c] = chains.get(c, 0) + w
        pct = w / total_weight * 100
        if pct > 12:
            warnings.append(f"{p.get('ticker','?')}: {pct:.1f}% concentration >12%")
    for s, w in sectors.items():
        pct = w / total_weight * 100
        if pct > 25:
            warnings.append(f"sector {s}: {pct:.1f}% >25%")
    return {
        "total_weight": total_weight, "sector_exposure": sectors,
        "chain_exposure": chains, "position_count": len(positions),
        "concentration_warnings": warnings,
        "real_trade_allowed": False, "broker_order_allowed": False,
    }
