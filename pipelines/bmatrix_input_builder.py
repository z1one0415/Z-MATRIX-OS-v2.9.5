"""Unified BMatrixInput builder — shared by Z-G13 and Z-G14"""
from __future__ import annotations
from typing import Callable


def build_bmatrix_input(ticker: str, name: str = "",
                        market_truth_fn: Callable | None = None,
                        get_financials_fn: Callable | None = None,
                        dq_score_fn: Callable | None = None,
                        l4_health_fn: Callable | None = None):
    """Build BMatrixInput from available data sources. Degrades gracefully."""
    try:
        from zmatrix.scoring.b_matrix import BMatrixInput
    except ImportError:
        return None

    g1 = market_truth_fn(ticker) if market_truth_fn else {}
    fin = get_financials_fn(ticker) if get_financials_fn else {}
    dq = dq_score_fn(ticker) if dq_score_fn else {"total": 0}
    l4 = l4_health_fn(ticker) if l4_health_fn else {"status": "stub"}

    return BMatrixInput(
        symbol=ticker,
        name=name or g1.get("name", ""),
        industry=g1.get("industry", fin.get("industry", "")),
        is_state_owned=fin.get("is_state_owned", g1.get("is_state_owned", False)),
        is_market_leader=g1.get("is_market_leader", False),
        is_st=g1.get("is_st", False),
        suspended=l4.get("status") == "BLOCK",
        delisting_risk=bool(l4.get("delisting_risk")),
        # Profitability
        roe_5y=fin.get("roe_5y_avg"),
        roe_trend=fin.get("roe_trend"),
        roic_5y=fin.get("roic_5y"),
        roic_trend=fin.get("roic_trend"),
        gross_margin=fin.get("gross_margin"),
        gross_margin_stability=fin.get("gross_margin_stability"),
        # Valuation
        pe_ttm=fin.get("pe_ttm"),
        pb=fin.get("pb"),
        profit_percentile_5y=fin.get("profit_percentile_5y"),
        # Balance sheet
        debt_ratio=fin.get("debt_ratio"),
        goodwill_to_net_assets=fin.get("goodwill_to_net_assets", fin.get("goodwill_ratio")),
        interest_bearing_debt_growth_2y=fin.get("interest_bearing_debt_growth_2y"),
        # Dividend
        dividend_yield=fin.get("dividend_yield"),
        dividend_years_stable=fin.get("dividend_years_stable"),
        dividends_paid_2y=fin.get("dividends_paid_2y"),
        capex_2y=fin.get("capex_2y"),
        ocf_2y=fin.get("ocf_2y"),
        # Time-series
        ocf_3y=fin.get("ocf_3y"),
        net_profit_3y=fin.get("net_profit_3y"),
        # Qualitative
        policy_stability_score=fin.get("policy_stability_score"),
        asset_monopoly_score=fin.get("asset_monopoly_score"),
        cost_curve_score=fin.get("cost_curve_score"),
        resource_quality_score=fin.get("resource_quality_score"),
        # Brand scarcity (B5)
        brand_premium_score=fin.get("brand_premium_score"),
        pricing_power_score=fin.get("pricing_power_score"),
        supply_constraint_score=fin.get("supply_constraint_score"),
        scarcity_durability_score=fin.get("scarcity_durability_score"),
        brand_mindshare_score=fin.get("brand_mindshare_score"),
        channel_health_score=fin.get("channel_health_score"),
        batch_price_trend_score=fin.get("batch_price_trend_score"),
        channel_inventory_risk_score=fin.get("channel_inventory_risk_score"),
        capex_reinvestment_need=fin.get("capex_reinvestment_need"),
        reinvestment_runway_score=fin.get("reinvestment_runway_score"),
        policy_consumption_risk_score=fin.get("policy_consumption_risk_score"),
        demand_generation_risk_score=fin.get("demand_generation_risk_score"),
        terminal_price_stability_score=fin.get("terminal_price_stability_score"),
        young_consumer_relevance_score=fin.get("young_consumer_relevance_score"),
        # Data completeness
        data_completeness=fin.get("financial_coverage_ratio", 0.0),
        extra={
            "financial_missing_fields": fin.get("missing_fields", []),
            "b5_missing_fields": fin.get("b5_missing_fields", []),
            "b5_evidence_coverage_ratio": fin.get("b5_evidence_coverage_ratio"),
        },
    )
