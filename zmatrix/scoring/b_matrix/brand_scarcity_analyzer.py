from __future__ import annotations
from .contracts import BMatrixInput, TrapFlag, TrapSeverity
from .shareholder_return_analyzer import clamp


def brand_scarcity_fit_score(stock: BMatrixInput) -> float:
    """Classifier helper: high score means brand scarcity type, not normal reinvestment compounding."""
    brand = stock.brand_premium_score if stock.brand_premium_score is not None else 5.0
    pricing = stock.pricing_power_score if stock.pricing_power_score is not None else 5.0
    supply = stock.supply_constraint_score if stock.supply_constraint_score is not None else 5.0
    gm = 5.0
    if stock.gross_margin is not None:
        gm = clamp((stock.gross_margin - 30.0) / 50.0 * 10.0)
    reinvestment_need = stock.capex_reinvestment_need if stock.capex_reinvestment_need is not None else 5.0
    low_reinvestment = 10.0 - reinvestment_need
    return brand * 0.25 + pricing * 0.25 + supply * 0.20 + gm * 0.15 + low_reinvestment * 0.15


def channel_health_score(stock: BMatrixInput) -> tuple[float, list[TrapFlag], list[str]]:
    score = stock.channel_health_score if stock.channel_health_score is not None else 5.0
    flags: list[str] = []
    traps: list[TrapFlag] = []
    if stock.batch_price_trend_score is not None:
        score = score * 0.55 + stock.batch_price_trend_score * 0.45
        if stock.batch_price_trend_score < 4.0:
            flags.append("batch_price_weakness")
    if stock.channel_inventory_risk_score is not None:
        # high risk score means riskier; invert it.
        inv = 10.0 - stock.channel_inventory_risk_score
        score = score * 0.75 + inv * 0.25
        if stock.channel_inventory_risk_score >= 7.5:
            traps.append(TrapFlag("CHANNEL_INVENTORY_RISK", "channel inventory risk is high", TrapSeverity.CAP_B))
    if stock.terminal_price_stability_score is not None:
        score = score * 0.80 + stock.terminal_price_stability_score * 0.20
    return clamp(score), traps, flags


def policy_demand_risk_score(stock: BMatrixInput) -> tuple[float, list[TrapFlag], list[str]]:
    policy_risk = stock.policy_consumption_risk_score if stock.policy_consumption_risk_score is not None else 4.0
    gen_risk = stock.demand_generation_risk_score if stock.demand_generation_risk_score is not None else 4.0
    young = stock.young_consumer_relevance_score if stock.young_consumer_relevance_score is not None else 5.0
    # lower risk and higher younger consumer relevance are better.
    score = (10.0 - policy_risk) * 0.40 + (10.0 - gen_risk) * 0.30 + young * 0.30
    traps: list[TrapFlag] = []
    flags: list[str] = []
    if policy_risk >= 8.0:
        traps.append(TrapFlag("POLICY_CONSUMPTION_RISK", "policy/official consumption pressure is high", TrapSeverity.CAP_B))
    if gen_risk >= 8.0:
        traps.append(TrapFlag("DEMAND_GENERATION_RISK", "generation demand risk is high", TrapSeverity.CAP_B))
    if young < 3.5:
        flags.append("young_consumer_relevance_weak")
    return clamp(score), traps, flags
