"""☯️ Portfolio Exposure v1.0 — 组合暴露分析器 (v2.9.8-dev)"""
from __future__ import annotations
from datetime import datetime

def analyze_portfolio_exposure(candidate: dict, portfolio: list[dict] | None = None) -> dict:
    now = datetime.now()
    portfolio = portfolio or []
    ticker = candidate.get("ticker", "UNKNOWN")
    chain = candidate.get("chain", "UNKNOWN")
    sector = candidate.get("sector", "UNKNOWN")
    style = candidate.get("style_factor", "UNKNOWN")
    add_weight = 5.0

    market_beta = candidate.get("market_beta")
    sector_beta = candidate.get("sector_beta")
    max_drawdown = candidate.get("max_drawdown")
    drawdown_overlap = candidate.get("drawdown_overlap")
    corr_60d = candidate.get("correlation_60d")
    corr_120d = candidate.get("correlation_120d")
    corr_250d = candidate.get("correlation_250d")

    beta_fields = [market_beta, sector_beta, max_drawdown, corr_60d, corr_120d, corr_250d]
    history_available = sum(1 for f in beta_fields if f is not None) >= 3

    warnings = []
    same_chain_weight = sum(p.get("weight", 0) for p in portfolio if p.get("chain") == chain and p.get("ticker") != ticker)
    same_sector_weight = sum(p.get("weight", 0) for p in portfolio if p.get("sector") == sector and p.get("ticker") != ticker)
    same_style_weight = sum(p.get("weight", 0) for p in portfolio if p.get("style_factor") == style and p.get("ticker") != ticker)

    total_chain = same_chain_weight + add_weight
    total_sector = same_sector_weight + add_weight
    duplicate_exposure = 0.0

    if total_chain > 35:
        warnings.append(f"CHAIN_EXPOSURE: {same_chain_weight:.1f}+{add_weight}={total_chain:.1f}>35"); duplicate_exposure = max(duplicate_exposure, total_chain)
    if total_sector > 35:
        warnings.append(f"SECTOR_EXPOSURE: {same_sector_weight:.1f}+{add_weight}={total_sector:.1f}>35"); duplicate_exposure = max(duplicate_exposure, total_sector)
    if same_style_weight + add_weight > 35:
        warnings.append(f"STYLE_EXPOSURE: {same_style_weight:.1f}+{add_weight}={same_style_weight+add_weight:.1f}>35")
        duplicate_exposure = max(duplicate_exposure, same_style_weight + add_weight)

    if not history_available:
        warnings.append("INSUFFICIENT_5Y_EXPOSURE_DATA")
        if not warnings:
            duplicate_exposure = max(duplicate_exposure, 100)

    degraded = not history_available
    exposure_gate_passed = len(warnings) == 0

    return {
        "exposure_version": "v1.0", "ticker": ticker,
        "chain": chain, "sector": sector, "style_factor": style,
        "current_weight_pct": add_weight,
        "duplicate_exposure_pct": round(duplicate_exposure, 1),
        "same_chain_weight_pct": round(same_chain_weight, 1),
        "same_sector_weight_pct": round(same_sector_weight, 1),
        "market_beta": market_beta, "sector_beta": sector_beta,
        "max_drawdown": max_drawdown, "drawdown_overlap": drawdown_overlap,
        "correlation_60d": corr_60d, "correlation_120d": corr_120d, "correlation_250d": corr_250d,
        "degraded": degraded,
        "exposure_gate_passed": exposure_gate_passed,
        "add_position_allowed": exposure_gate_passed and not degraded,
        "warnings": warnings, "real_trade_allowed": False,
    }
