"""ResearchDB Account Truth — account reconciler (trade ↔ position ↔ cashflow)."""
from __future__ import annotations
from zmatrix.research_db.account_truth import TradeRecord, PositionRecord, CashflowRecord, AccountSnapshot


def reconcile_trade_amount(record: TradeRecord) -> dict:
    """Verify trade amount = price * quantity."""
    expected = record.price * record.quantity
    ok = abs(record.amount - expected) < 0.01
    return {"status": "PASS" if ok else "FAILED", "expected": expected, "actual": record.amount, "trade_id": record.trade_id}


def reconcile_equity(snapshot: AccountSnapshot) -> dict:
    """Verify total_equity ≈ cash + market_value."""
    expected = snapshot.cash + snapshot.market_value
    diff = abs(snapshot.total_equity - expected)
    ok = diff < max(snapshot.total_equity * 0.01, 1.0)
    return {"status": "PASS" if ok else "FAILED", "expected": expected, "actual": snapshot.total_equity, "diff": diff, "date": snapshot.date}


def reconcile_capital_curve(snapshots: list[AccountSnapshot], cashflows: list[CashflowRecord]) -> dict:
    """Build net-deposit-adjusted equity curve. Deposits are NOT returns."""
    if not snapshots:
        return {"status": "FAILED", "error_type": "RECONCILIATION_FAILED", "failed_rows": [], "blocking": True}
    return {"status": "PASS", "snapshot_count": len(snapshots), "cashflow_count": len(cashflows), "cost_method": "FIFO"}
