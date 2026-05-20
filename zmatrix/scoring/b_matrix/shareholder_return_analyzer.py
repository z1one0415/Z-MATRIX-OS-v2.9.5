from __future__ import annotations
from .contracts import BMatrixInput


def clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


def dividend_yield_score(dy: float | None) -> float:
    if dy is None:
        return 5.0
    if dy <= 0:
        return 3.0
    if dy >= 4:
        return 10.0
    if dy >= 2:
        return 7.0 + (dy - 2.0) / 2.0 * 3.0
    return 5.0


def fcf_dividend_coverage_score(stock: BMatrixInput) -> float:
    if not stock.ocf_2y or not stock.capex_2y or not stock.dividends_paid_2y:
        return 5.0
    fcf = sum(stock.ocf_2y) - sum(stock.capex_2y)
    divs = sum(stock.dividends_paid_2y)
    if divs <= 0:
        return 5.0
    ratio = fcf / divs
    return clamp(3.0 + ratio * 3.5)


def shareholder_return_score(stock: BMatrixInput) -> float:
    dy = dividend_yield_score(stock.dividend_yield)
    years = stock.dividend_years_stable or 0
    stability = clamp(3.0 + min(years, 10) * 0.7)
    fcf_cov = fcf_dividend_coverage_score(stock)
    buyback = stock.buyback_quality_score if stock.buyback_quality_score is not None else 5.0
    payout_safety = 5.0
    return dy * 0.30 + stability * 0.25 + fcf_cov * 0.25 + payout_safety * 0.10 + buyback * 0.10
