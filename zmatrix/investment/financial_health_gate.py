"""☯️ 个股健康硬门 v1.0 (v2.9.8-dev)

只有通过此门的数据才能进入 B-Matrix 长期底仓评估。
信息不足不能 PASS，只能 DEGRADED。
只判资格，不给买卖建议。
"""
from __future__ import annotations
from datetime import datetime

HARD_GATE_FIELDS = [
    "revenue_growth", "net_profit_growth", "deducted_net_profit_growth",
    "gross_margin", "operating_cashflow", "roe", "debt_ratio",
    "valuation_percentile", "goodwill_risk", "receivable_risk", "inventory_risk",
]
_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}

def check_financial_health(candidate: dict, fundamentals: dict | None = None) -> dict:
    now = datetime.now()
    fd = fundamentals or candidate.get("fundamentals", {})
    ticker = candidate.get("ticker", fd.get("ticker", "UNKNOWN"))
    available = sum(1 for f in HARD_GATE_FIELDS if fd.get(f) is not None)
    degraded = available < 5
    failed_items = []
    warnings = []

    if not degraded:
        if fd.get("revenue_growth") is not None and fd["revenue_growth"] < -20:
            failed_items.append("revenue_growth < -20%")
        if fd.get("net_profit_growth") is not None and fd["net_profit_growth"] < -30:
            failed_items.append("net_profit_growth < -30%")
        if fd.get("deducted_net_profit_growth") is not None and fd["deducted_net_profit_growth"] < -30:
            failed_items.append("deducted_net_profit_growth < -30%")
        if fd.get("gross_margin") is not None and fd["gross_margin"] < 20:
            failed_items.append("gross_margin < 20%")
        if fd.get("operating_cashflow") is not None and fd["operating_cashflow"] < 0:
            failed_items.append("operating_cashflow negative")
        if fd.get("roe") is not None and fd["roe"] < 5:
            failed_items.append("roe < 5%")
        if fd.get("debt_ratio") is not None and fd["debt_ratio"] > 70:
            failed_items.append("debt_ratio > 70%")
        if fd.get("valuation_percentile") is not None and fd["valuation_percentile"] > 90:
            failed_items.append("valuation_percentile > 90%")
    else:
        warnings.append(f"insufficient data: {available}/{len(HARD_GATE_FIELDS)}")

    financial_gate_passed = not degraded and len(failed_items) == 0

    return {
        "module": "financial.health_gate", "version": "v1.0",
        "ticker": ticker,
        "financial_gate_passed": financial_gate_passed,
        "degraded": degraded, "failed_items": failed_items,
        "warnings": warnings, "real_trade_allowed": False,
    }
