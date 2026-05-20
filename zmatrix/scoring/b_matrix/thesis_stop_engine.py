from __future__ import annotations
from .contracts import BMatrixInput, BaseType


def evaluate_thesis_stop(stock: BMatrixInput, snapshot: dict) -> dict:
    triggers: list[str] = []
    assumptions = snapshot.get("core_assumptions", {}) if snapshot else {}
    base_type = snapshot.get("base_type") if snapshot else None

    roe_mid = assumptions.get("roe_midline")
    if roe_mid is not None and stock.roe_5y is not None and stock.roe_5y < roe_mid * 0.75:
        triggers.append("roe_midline_materially_broken")

    if stock.ocf_3y and stock.net_profit_3y and sum(stock.net_profit_3y) > 0:
        if sum(stock.ocf_3y) / sum(stock.net_profit_3y) < 0.7:
            triggers.append("ocf_ni_3y_below_0_7")

    if stock.extra.get("dividend_cut_without_capex_reason"):
        triggers.append("dividend_cut_without_capex_reason")
    if stock.extra.get("industry_policy_destroyed"):
        triggers.append("industry_policy_destroyed")

    if base_type == BaseType.BRAND_SCARCITY_MONOPOLY.value or base_type == "BRAND_SCARCITY_MONOPOLY":
        if stock.channel_health_score is not None and stock.channel_health_score < 4:
            triggers.append("brand_channel_health_broken")
        if stock.batch_price_trend_score is not None and stock.batch_price_trend_score < 4:
            triggers.append("batch_price_trend_broken")
        if stock.pricing_power_score is not None and stock.pricing_power_score < 6:
            triggers.append("pricing_power_weakened")
        if stock.policy_consumption_risk_score is not None and stock.policy_consumption_risk_score >= 8:
            triggers.append("policy_consumption_risk_high")

    status = "THESIS_BROKEN" if triggers else "THESIS_INTACT"
    return {"status": status, "triggers": triggers}
