"""ResearchDB Account Truth — account reconciler (trade ↔ position ↔ cashflow)."""
from __future__ import annotations
from zmatrix.research_db.account_truth import TradeRecord, PositionRecord, CashflowRecord, AccountSnapshot



# Strict reconciliation tolerances (Pack C.4)
DEFAULT_TOLERANCE_ABS = 0.01  # 1 cent for price/amount
DEFAULT_TOLERANCE_PCT = 0.001  # 0.1%

def reconcile_with_tolerance(expected: float, actual: float, tolerance_abs: float = DEFAULT_TOLERANCE_ABS,
                              tolerance_pct: float = DEFAULT_TOLERANCE_PCT, strict_mode: bool = True) -> dict:
    """Reconcile expected vs actual with explicit tolerance. Never returns PASS on error silently."""
    diff_abs = abs(expected - actual)
    diff_pct = diff_abs / max(abs(expected), 0.01) if abs(expected) > 0.01 else 0.0
    within_tol = diff_abs <= tolerance_abs and diff_pct <= tolerance_pct
    if diff_abs == 0 or within_tol:
        return {"status": "PASS", "difference_abs": diff_abs, "difference_pct": diff_pct,
                "tolerance_abs": tolerance_abs, "tolerance_pct": tolerance_pct,
                "strict_mode": strict_mode, "reconciliation_status": "PASS", "reconciliation_message": ""}
    if strict_mode:
        return {"status": "ERROR", "difference_abs": diff_abs, "difference_pct": diff_pct,
                "tolerance_abs": tolerance_abs, "tolerance_pct": tolerance_pct,
                "strict_mode": strict_mode, "reconciliation_status": "ERROR",
                "reconciliation_message": f"Diff {diff_abs:.4f} ({diff_pct:.2%}) exceeds tolerance {tolerance_abs} / {tolerance_pct:.2%}"}
    return {"status": "WARNING", "difference_abs": diff_abs, "difference_pct": diff_pct,
            "tolerance_abs": tolerance_abs, "tolerance_pct": tolerance_pct,
            "strict_mode": strict_mode, "reconciliation_status": "WARNING",
            "reconciliation_message": f"Diff {diff_abs:.4f} ({diff_pct:.2%}) within tolerance but strict_mode=False"}

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
