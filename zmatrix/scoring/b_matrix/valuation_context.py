from __future__ import annotations
from .contracts import BMatrixInput, BaseType, TrapFlag, TrapSeverity
from .shareholder_return_analyzer import clamp


def generic_pe_score(pe: float | None) -> float:
    if pe is None or pe <= 0:
        return 5.0
    if pe < 10:
        return 9.0
    if pe < 20:
        return 7.0 + (20 - pe) / 10.0 * 2.0
    if pe < 30:
        return 5.0 + (30 - pe) / 10.0 * 2.0
    if pe < 40:
        return 3.0 + (40 - pe) / 10.0 * 2.0
    return 2.0


def pb_roe_cross_check(stock: BMatrixInput) -> tuple[float, list[str]]:
    adj = 0.0
    flags: list[str] = []
    pb = stock.pb
    roe = stock.roe_5y
    if pb is None or roe is None:
        return adj, flags
    if pb < 1.0 and roe < 5:
        adj -= 3.0
        flags.append("LOW_PB_LOW_ROE_TRAP")
    if pb < 1.5 and roe > 10:
        adj += 1.0
        flags.append("PB_ROE_TRUE_UNDERVALUE_HINT")
    if pb > 5.0 and roe < 10:
        adj -= 2.0
        flags.append("HIGH_PB_LOW_ROE_TRAP")
    return adj, flags


def valuation_score_by_type(stock: BMatrixInput, base_type: BaseType) -> tuple[float, list[TrapFlag], list[str]]:
    traps: list[TrapFlag] = []
    flags: list[str] = []
    if base_type == BaseType.RESOURCE_CASH_COW:
        pe = stock.pe_ttm
        score = 5.0
        if stock.pb is not None:
            score += (1.5 - min(stock.pb, 3.0)) * 1.2
        if stock.ev_ebitda is not None:
            score += (8 - min(stock.ev_ebitda, 12)) * 0.25
        if pe is not None and pe < 5 and (stock.profit_percentile_5y or 0) > 0.85 and (stock.commodity_price_percentile or 0) > 0.80:
            traps.append(TrapFlag("CYCLICAL_PEAK_EARNINGS_TRAP", "Low PE at profit/commodity high percentile", TrapSeverity.CAP_B))
            flags.append("cyclical_peak_low_pe_warning")
            score -= 2.5
        return clamp(score), traps, flags

    if base_type in {BaseType.HIGH_DIVIDEND_ANCHOR, BaseType.STATE_INFRA_MONOPOLY}:
        score = generic_pe_score(stock.pe_ttm) * 0.45
        pb_score = 5.0 if stock.pb is None else clamp(8.0 - (stock.pb - 1.0) * 2.0)
        score += pb_score * 0.55
        adj, f = pb_roe_cross_check(stock)
        flags.extend(f)
        return clamp(score + adj), traps, flags

    if base_type == BaseType.BRAND_SCARCITY_MONOPOLY:
        # Scarce brands can deserve premium valuation, but premium must be supported by channel health and growth stability.
        pe_score = generic_pe_score(stock.pe_ttm)
        pricing_bonus = 0.0
        if stock.pricing_power_score is not None:
            pricing_bonus += clamp((stock.pricing_power_score - 6.0) / 4.0 * 1.5, -1.0, 1.5)
        if stock.channel_health_score is not None and stock.channel_health_score < 4.0:
            flags.append("premium_valuation_channel_health_mismatch")
            pricing_bonus -= 1.5
        adj, f = pb_roe_cross_check(stock)
        flags.extend(f)
        return clamp(pe_score + pricing_bonus + adj), traps, flags

    # Compounding reinvestment tolerates higher PE if return quality is strong.
    pe_score = generic_pe_score(stock.pe_ttm)
    roic_bonus = 0.0
    if stock.roic_5y is not None:
        roic_bonus = clamp((stock.roic_5y - 10) / 10 * 2.0, -1.0, 2.0)
    adj, f = pb_roe_cross_check(stock)
    flags.extend(f)
    return clamp(pe_score + roic_bonus + adj), traps, flags
