"""ResearchDB Account Truth — account truth report generator."""
from __future__ import annotations


def generate_account_truth_report(
    trades_count: int = 0, positions_count: int = 0,
    snapshots_count: int = 0, cashflows_count: int = 0,
    drawdowns: list[dict] | None = None, holdings: list[dict] | None = None,
) -> str:
    """Generate an account truth markdown report."""
    lines = [
        "# Account Truth Report",
        "",
        "## Summary",
        f"- Total trades: {trades_count}",
        f"- Position records: {positions_count}",
        f"- Account snapshots: {snapshots_count}",
        f"- Cashflow records: {cashflows_count}",
        "",
        "## Drawdowns",
    ]
    if drawdowns:
        for d in drawdowns:
            lines.append(f"- {d.get('start_date','?')} → {d.get('end_date','?')}: {d.get('drawdown_pct',0):.2%}")
    else:
        lines.append("- No drawdown data")
    
    lines.extend(["", "## Holdings", ""])
    if holdings:
        total_pnl = sum(h.get("realized_pnl", 0) for h in holdings)
        lines.append(f"- Total realized PnL: {total_pnl:,.2f}")
        for h in holdings:
            lines.append(f"- {h['ticker']} {h.get('name','')}: PnL={h.get('realized_pnl',0):,.2f} Return={h.get('total_return',0):.2%}")
    
    lines.extend(["", "## Safety", "- Production: BLOCKED", "- Report type: Paper-only"])
    return "\n".join(lines)
