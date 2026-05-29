# allowlist: forbidden-token-definition
"""Exposure Report — full portfolio exposure with all risk metrics"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.portfolio_exposure.exposure_calculator import calc_exposure
from zmatrix.portfolio_exposure.concentration_checker import check_concentration
from zmatrix.portfolio_exposure.max_loss_budget import calc_max_loss_budget


def build_exposure_report(positions: list[dict],
                           prices_map: dict[str, list[float]] | None = None,
                           index_prices: list[float] | None = None) -> dict:
    """Build full portfolio exposure report with all risk components."""
    # Normalize positions
    from zmatrix.portfolio_exposure.position_normalizer import normalize_positions
    normalized = normalize_positions(positions)

    # Core exposure
    exposure = calc_exposure(normalized)

    # Single-name exposure
    single_name = []
    total_w = exposure["total_weight"] or 1.0
    for p in normalized:
        w = p.get("weight", 0) / total_w * 100
        beta = p.get("beta", 1.0)
        single_name.append({
            "ticker": p.get("ticker"), "role": p.get("role"),
            "weight_pct": round(w, 1),
            "beta": beta,
            "beta_adjusted_exposure": round(w * beta, 1),
            "current_price": p.get("current_price"),
            "entry_price": p.get("entry_price"),
        })

    # Concentration
    concentration = check_concentration(normalized)

    # Beta exposure
    beta_exposure = {}
    if index_prices and prices_map:
        from zmatrix.portfolio_exposure.beta_calculator import calc_beta
        for p in normalized:
            stock_prices = prices_map.get(p["ticker"])
            if stock_prices and index_prices:
                b = calc_beta(stock_prices, index_prices)
                if b is not None:
                    beta_exposure[p["ticker"]] = b

    # Correlation risk
    corr_matrix = {}
    if prices_map:
        from zmatrix.portfolio_exposure.correlation_calculator import build_correlation_matrix
        corr_matrix = build_correlation_matrix(normalized, prices_map)

    # Max loss
    max_loss = calc_max_loss_budget(normalized)

    seed = f"exposure_report|{len(normalized)}|{datetime.now(timezone.utc).isoformat()}"
    report_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "report_version": "EXPOSURE_REPORT_V10",
        "report_id": report_id,
        "created_at": created_at,
        "position_count": len(normalized),
        "single_name_exposure": single_name,
        "sector_exposure": exposure["sector_exposure"],
        "chain_exposure": exposure["chain_exposure"],
        "beta_exposure": beta_exposure,
        "correlation_risk": corr_matrix,
        "concentration_warnings": concentration["warnings"],
        "concentration_breach_count": concentration["breach_count"],
        "max_loss_budget": max_loss,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "auto_sell_allowed": False, "auto_position_close_allowed": False,
    }
