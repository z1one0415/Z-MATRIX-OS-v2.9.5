from __future__ import annotations
from .base_pricer import BaseBMatrixPricer
from ..contracts import BMatrixInput, BaseType, TrapFlag
from ..valuation_context import valuation_score_by_type
from ..shareholder_return_analyzer import shareholder_return_score
from ..moat_analyzer import brand_scarcity_moat_score
from ..brand_scarcity_analyzer import channel_health_score, policy_demand_risk_score


class BrandScarcityMonopolyPricer(BaseBMatrixPricer):
    """B5: Brand scarcity monopoly cash cow.

    Example archetype: premium baijiu with geographic/process scarcity and pricing power.
    This is not a standard reinvestment compounder.
    """
    base_type = BaseType.BRAND_SCARCITY_MONOPOLY

    def weighted_score(self, stock: BMatrixInput):
        traps: list[TrapFlag] = []
        valuation, val_traps, val_flags = valuation_score_by_type(stock, self.base_type)
        traps.extend(val_traps)

        pricing = stock.pricing_power_score if stock.pricing_power_score is not None else 5.0
        scarcity = stock.scarcity_durability_score if stock.scarcity_durability_score is not None else stock.supply_constraint_score or 5.0
        brand = stock.brand_mindshare_score if stock.brand_mindshare_score is not None else stock.brand_premium_score or 5.0
        channel, channel_traps, channel_flags = channel_health_score(stock)
        traps.extend(channel_traps)
        cash = shareholder_return_score(stock)
        moat = brand_scarcity_moat_score(stock)
        policy_demand, risk_traps, risk_flags = policy_demand_risk_score(stock)
        traps.extend(risk_traps)

        # B5 full parameter design:
        # Pricing Power 25%, Scarcity Durability 20%, Brand Mindshare 20%,
        # Channel Health 15%, Cash Conversion/Shareholder Return 10%,
        # Policy/Demand Risk 10%.
        score = (
            pricing * 0.25
            + scarcity * 0.20
            + brand * 0.20
            + channel * 0.15
            + cash * 0.10
            + policy_demand * 0.10
        )
        quality_flags = channel_flags + risk_flags
        if moat < 6.0:
            quality_flags.append("brand_scarcity_moat_not_confirmed")
        secondary_traits = ["SHAREHOLDER_RETURN_CASH_COW", "MATURE_BRAND_COMPOUNDER"]
        return score, traps, val_flags, quality_flags, secondary_traits
