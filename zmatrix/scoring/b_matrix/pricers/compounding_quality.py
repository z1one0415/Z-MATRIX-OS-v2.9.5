from __future__ import annotations
from .base_pricer import BaseBMatrixPricer, score_stability_roe, clamp
from ..contracts import BMatrixInput, BaseType, TrapFlag
from ..valuation_context import valuation_score_by_type
from ..moat_analyzer import moat_score


class CompoundingQualityPricer(BaseBMatrixPricer):
    base_type = BaseType.COMPOUNDING_QUALITY

    def weighted_score(self, stock: BMatrixInput):
        traps: list[TrapFlag] = []
        valuation, val_traps, val_flags = valuation_score_by_type(stock, self.base_type)
        traps.extend(val_traps)
        roic = stock.roic_5y if stock.roic_5y is not None else stock.roe_5y
        roic_score = score_stability_roe(roic)
        revenue_quality = stock.extra.get("revenue_profit_quality_score", 5.0)
        cashflow = 5.0
        if stock.ocf_3y and stock.net_profit_3y and sum(stock.net_profit_3y) > 0:
            cashflow = clamp(3.0 + (sum(stock.ocf_3y) / sum(stock.net_profit_3y)) * 4.0)
        moat = moat_score(stock)
        reinvestment = stock.reinvestment_runway_score if stock.reinvestment_runway_score is not None else 5.0
        score = roic_score * 0.23 + revenue_quality * 0.17 + cashflow * 0.18 + moat * 0.17 + reinvestment * 0.10 + valuation * 0.15
        q_flags = []
        if stock.roic_trend == "down":
            q_flags.append("roic_declining_watch")
            score -= 0.8
        return score, traps, val_flags, q_flags, ["REINVESTMENT_COMPOUNDER"]
