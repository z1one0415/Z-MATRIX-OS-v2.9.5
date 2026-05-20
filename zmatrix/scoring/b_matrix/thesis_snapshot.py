from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date
from .contracts import BMatrixInput, BaseType


@dataclass
class ThesisSnapshot:
    symbol: str
    base_type: str
    thesis_date: str
    core_assumptions: dict
    thesis_stop_rules: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _brand_scarcity_rules() -> list[str]:
    return [
        "channel_health_score < 4 for 2 consecutive checks",
        "batch_price_trend_score < 4 and inventory risk rises",
        "pricing_power_score falls below 6",
        "brand_mindshare_score materially deteriorates",
        "policy_consumption_risk_score >= 8",
        "OCF/NI 3y < 0.7",
        "dividend cut without capex or policy explanation",
    ]


def build_thesis_snapshot(stock: BMatrixInput, base_type: BaseType) -> ThesisSnapshot:
    assumptions = {
        "roe_midline": stock.roe_5y,
        "roic_midline": stock.roic_5y,
        "ocf_ni_3y_min": 0.7,
        "dividend_policy": "stable_or_rising" if (stock.dividend_yield or 0) > 0 else "not_core",
        "max_debt_ratio": stock.debt_ratio,
        "moat_key": "asset_or_cashflow_durability",
        "industry_thesis": stock.industry,
    }
    if base_type == BaseType.BRAND_SCARCITY_MONOPOLY:
        assumptions.update({
            "moat_key": "brand_scarcity_pricing_power",
            "pricing_power_min": 6.0,
            "channel_health_min": 4.0,
            "brand_mindshare_min": 6.0,
            "policy_consumption_risk_max": 8.0,
        })
        rules = _brand_scarcity_rules()
    else:
        rules = [
            "ocf_ni_3y < 0.7",
            "dividend_cut_without_capex_reason",
            "roe_or_roic_midline_breaks_for_2_reports",
            "industry_policy_destroyed",
            "balance_sheet_deteriorates",
        ]
    return ThesisSnapshot(stock.symbol, base_type.value, date.today().isoformat(), assumptions, rules)
