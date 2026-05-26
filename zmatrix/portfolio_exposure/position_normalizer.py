"""Position Normalizer — unify positions from multiple sources"""
from __future__ import annotations

def normalize_positions(raw_positions: list[dict]) -> list[dict]:
    """Normalize raw position dicts into standard format."""
    out = []
    for i, p in enumerate(raw_positions):
        out.append({
            "position_id": p.get("position_id", f"pos_{i}"),
            "ticker": p.get("ticker", ""),
            "role": p.get("role", "UNKNOWN"),
            "weight": float(p.get("weight", 0)),
            "entry_price": float(p.get("entry_price", 0) or 0),
            "current_price": float(p.get("current_price", 0) or 0),
            "beta": float(p.get("beta", 1.0) or 1.0),
            "sector": p.get("sector", "unknown"),
            "chain": p.get("chain", "unknown"),
            "exposure_ratio": float(p.get("exposure_ratio", 0) or 0),
        })
    return out
