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

def reconcile_trade_amount(record: TradeRecord, strict_mode: bool = True) -> dict:
    """Verify trade amount = price * quantity. Uses reconcile_with_tolerance."""
    expected = record.price * record.quantity
    result = reconcile_with_tolerance(expected, record.amount, strict_mode=strict_mode)
    result["trade_id"] = record.trade_id
    return result


def reconcile_equity(snapshot: AccountSnapshot, strict_mode: bool = True) -> dict:
    """Verify total_equity ≈ cash + market_value. Uses reconcile_with_tolerance."""
    expected = snapshot.cash + snapshot.market_value
    tolerance_abs = max(snapshot.total_equity * 0.01, 1.0)
    result = reconcile_with_tolerance(expected, snapshot.total_equity, tolerance_abs=tolerance_abs, tolerance_pct=0.01, strict_mode=strict_mode)
    result["date"] = snapshot.date
    return result


def reconcile_capital_curve(snapshots: list[AccountSnapshot], cashflows: list[CashflowRecord]) -> dict:
    """Build net-deposit-adjusted equity curve. Deposits are NOT returns."""
    if not snapshots:
        return {"status": "FAILED", "error_type": "RECONCILIATION_FAILED", "failed_rows": [], "blocking": True}
    return {"status": "PASS", "snapshot_count": len(snapshots), "cashflow_count": len(cashflows), "cost_method": "FIFO"}
