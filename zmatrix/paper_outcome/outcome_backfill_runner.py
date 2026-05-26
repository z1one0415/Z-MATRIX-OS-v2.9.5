"""Outcome Backfill Runner — compute full outcome from paper + price path"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.paper_outcome.return_calculator import calc_all_horizons
from zmatrix.paper_outcome.drawdown_calculator import calc_all_drawdowns
from zmatrix.paper_outcome.schema import DEFAULT_OUTCOME_SAFETY


def run_outcome_backfill(*, paper_entry: dict, price_path: list[float] | None = None) -> dict:
    """Compute full outcome for a paper trade entry."""
    entry_price = float(paper_entry.get("entry_price", 0) or 0)
    paper_id = paper_entry.get("paper_id", "")
    ticker = paper_entry.get("ticker", "")
    if price_path is None or entry_price <= 0:
        return {
            "paper_id": paper_id, "ticker": ticker,
            "entry_price": entry_price,
            "outcome_status": "INSUFFICIENT_DATA",
            "actual_return_t5": None, "actual_return_t20": None, "actual_return_t60": None,
            "max_drawdown_t20": None, "max_drawdown_t60": None,
            "safety": dict(DEFAULT_OUTCOME_SAFETY),
        }
    returns = calc_all_horizons(entry_price, price_path)
    drawdowns = calc_all_drawdowns(price_path)
    seed = f"{paper_id}|{entry_price}|{len(price_path)}"
    outcome_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "outcome_id": outcome_id, "paper_id": paper_id, "ticker": ticker,
        "entry_date": paper_entry.get("entry_date", ""),
        "entry_price": entry_price,
        "outcome_status": "READY",
        "actual_return_t5": returns.get("actual_return_t5"),
        "actual_return_t20": returns.get("actual_return_t20"),
        "actual_return_t60": returns.get("actual_return_t60"),
        "max_drawdown_t20": drawdowns.get("max_drawdown_t20"),
        "max_drawdown_t60": drawdowns.get("max_drawdown_t60"),
        "error_type": "", "review_note": "",
        "created_at": created_at,
        "max_loss_plan": paper_entry.get("max_loss_plan"),
        "invalidation_triggered": False,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "safety": dict(DEFAULT_OUTCOME_SAFETY),
    }
