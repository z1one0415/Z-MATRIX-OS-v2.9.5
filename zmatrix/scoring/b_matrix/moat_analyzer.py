from __future__ import annotations
from .contracts import BMatrixInput
from .shareholder_return_analyzer import clamp


def moat_score(stock: BMatrixInput) -> float:
    leader = 8.0 if stock.is_market_leader else 5.0
    margin_stability = stock.gross_margin_stability if stock.gross_margin_stability is not None else 5.0
    roe_persistence = 5.0
    if stock.roe_5y is not None:
        roe_persistence = clamp(5.0 + (stock.roe_5y - 8) / 12 * 5.0)
    industry_barrier = stock.asset_monopoly_score if stock.asset_monopoly_score is not None else (6.0 if stock.is_state_owned else 5.0)
    substitution = stock.substitution_risk_score if stock.substitution_risk_score is not None else 5.0
    return leader * 0.25 + margin_stability * 0.20 + roe_persistence * 0.20 + industry_barrier * 0.20 + substitution * 0.15


def brand_scarcity_moat_score(stock: BMatrixInput) -> float:
    """Brand scarcity moat is not state ownership; it is pricing power + scarcity + mindshare."""
    pricing = stock.pricing_power_score if stock.pricing_power_score is not None else 5.0
    scarcity = stock.scarcity_durability_score if stock.scarcity_durability_score is not None else stock.supply_constraint_score or 5.0
    mindshare = stock.brand_mindshare_score if stock.brand_mindshare_score is not None else stock.brand_premium_score or 5.0
    substitution = stock.substitution_risk_score if stock.substitution_risk_score is not None else 5.0
    channel = stock.channel_health_score if stock.channel_health_score is not None else 5.0
    return pricing * 0.30 + scarcity * 0.25 + mindshare * 0.25 + substitution * 0.10 + channel * 0.10
