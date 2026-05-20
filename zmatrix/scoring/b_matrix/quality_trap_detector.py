from __future__ import annotations
from .contracts import BMatrixInput, TrapFlag, TrapSeverity


def _safe_sum(xs):
    return None if xs is None else sum(x for x in xs if x is not None)


def _all_positive_widening(a, b) -> bool:
    if not a or not b or len(a) < 4 or len(b) < 4:
        return False
    diffs = [x - y for x, y in zip(a[-4:], b[-4:])]
    return all(d > 0 for d in diffs) and diffs[-1] >= diffs[0]


class QualityTrapDetector:
    """B21 quality trap detector with 3-year time-series penetration."""

    def detect(self, stock: BMatrixInput) -> list[TrapFlag]:
        traps: list[TrapFlag] = []
        ocf_sum = _safe_sum(stock.ocf_3y)
        ni_sum = _safe_sum(stock.net_profit_3y)
        if ocf_sum is not None and ni_sum and ni_sum > 0:
            ratio = ocf_sum / ni_sum
            if ratio < 0.7:
                traps.append(TrapFlag("EARNINGS_QUALITY_TRAP", f"3y OCF/NI={ratio:.2f}<0.70", TrapSeverity.CAP_C))
            elif ratio < 0.9:
                traps.append(TrapFlag("CASHFLOW_WARNING", f"3y OCF/NI={ratio:.2f}<0.90", TrapSeverity.WARNING))

        if _all_positive_widening(stock.ar_growth_4q, stock.revenue_growth_4q):
            traps.append(TrapFlag("RECEIVABLES_INFLATION", "AR growth exceeds revenue growth for 4 quarters", TrapSeverity.CAP_B))

        if _all_positive_widening(stock.inventory_growth_4q, stock.cogs_growth_4q):
            traps.append(TrapFlag("INVENTORY_PRESSURE", "Inventory growth exceeds COGS growth for 4 quarters", TrapSeverity.CAP_B))

        if stock.goodwill_to_net_assets is not None and stock.goodwill_to_net_assets > 0.30:
            traps.append(TrapFlag("GOODWILL_RISK", "Goodwill/net assets > 30%", TrapSeverity.CAP_B))

        if stock.ocf_2y and stock.capex_2y and stock.dividends_paid_2y:
            fcf = sum(stock.ocf_2y) - sum(stock.capex_2y)
            divs = sum(stock.dividends_paid_2y)
            if divs > 0 and fcf - divs < 0 and (stock.interest_bearing_debt_growth_2y or 0) > 0:
                traps.append(TrapFlag("DEBT_FUNDED_DIVIDEND", "FCF fails to cover dividends while interest-bearing debt rises", TrapSeverity.CAP_C))

        if stock.is_st or stock.delisting_risk:
            traps.append(TrapFlag("NOT_INVESTMENT_GRADE", "ST or delisting risk", TrapSeverity.REJECT))
        return traps
