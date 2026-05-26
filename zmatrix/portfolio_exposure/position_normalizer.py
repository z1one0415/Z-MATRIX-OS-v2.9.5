"""Position Normalizer — unify positions, auto-calc weight from qty × price"""
from __future__ import annotations


def normalize_positions(raw_positions: list[dict], total_equity: float | None = None) -> list[dict]:
    """Normalize raw positions.

    - Reads weight directly if provided.
    - Automatically calculates weight = (quantity × current_price) / total_equity
      if weight is not provided and quantity + current_price are present.
    """
    out = []
    has_weights = all(p.get("weight") is not None and float(p.get("weight", 0)) > 0 for p in raw_positions)
    need_auto = not has_weights and all(
        p.get("quantity") and p.get("current_price") for p in raw_positions)

    if need_auto and total_equity is None:
        total_equity = sum(
            float(p.get("quantity", 0)) * float(p.get("current_price", 0))
            for p in raw_positions
        )
    total_equity = total_equity or 1.0

    for i, p in enumerate(raw_positions):
        quantity = float(p.get("quantity", 0) or 0)
        cur_price = float(p.get("current_price", 0) or 0)
        weight = float(p.get("weight", 0) or 0)

        if need_auto and quantity > 0 and cur_price > 0:
            weight = (quantity * cur_price) / total_equity

        out.append({
            "position_id": p.get("position_id", f"pos_{i}"),
            "ticker": p.get("ticker", ""),
            "role": p.get("role", "UNKNOWN"),
            "quantity": quantity,
            "weight": round(weight, 4),
            "entry_price": float(p.get("entry_price", 0) or 0),
            "current_price": cur_price,
            "beta": float(p.get("beta", 1.0) or 1.0),
            "sector": p.get("sector", "unknown"),
            "chain": p.get("chain", "unknown"),
            "exposure_ratio": float(p.get("exposure_ratio", 0) or 0),
            "max_loss_plan": float(p.get("max_loss_plan", 0) or 0),
        })
    return out
