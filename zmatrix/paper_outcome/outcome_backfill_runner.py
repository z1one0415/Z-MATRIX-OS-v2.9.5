"""Outcome Backfill Runner — full outcome with benchmark + invalidation"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.paper_outcome.return_calculator import calc_all_horizons
from zmatrix.paper_outcome.drawdown_calculator import calc_all_drawdowns, calc_entry_relative_drawdown
from zmatrix.paper_outcome.schema import DEFAULT_OUTCOME_SAFETY


def run_outcome_backfill(*, paper_entry: dict, price_path: list[float] | None = None,
                          benchmark_path: list[float] | None = None) -> dict:
    """Compute full outcome for a paper trade entry with benchmark + invalidation."""
    entry_price = float(paper_entry.get("entry_price", 0) or 0)
    paper_id = paper_entry.get("paper_id", "")
    ticker = paper_entry.get("ticker", "")
    max_loss_plan = float(paper_entry.get("max_loss_plan", 0) or 0)

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
    mae = calc_entry_relative_drawdown(entry_price, price_path)

    # Benchmark comparison
    excess_t5 = excess_t20 = excess_t60 = None
    if benchmark_path:
        from zmatrix.paper_outcome.benchmark_relative import calc_benchmark_comparison
        bm_returns = calc_all_horizons(benchmark_path[0] if benchmark_path else 0, benchmark_path)
        paper_returns = {"actual_return_t5": returns["actual_return_t5"],
                         "actual_return_t20": returns["actual_return_t20"],
                         "actual_return_t60": returns["actual_return_t60"]}
        bm_dict = {"bm_return_t5": bm_returns["actual_return_t5"],
                   "bm_return_t20": bm_returns["actual_return_t20"],
                   "bm_return_t60": bm_returns["actual_return_t60"]}
        excess = calc_benchmark_comparison(paper_returns, bm_dict)
        excess_t5 = excess.get("excess_return_t5")
        excess_t20 = excess.get("excess_return_t20")
        excess_t60 = excess.get("excess_return_t60")

    # Invalidation detection
    invalidation_triggered = False
    invalidation_reason = ""
    if max_loss_plan > 0:
        mae_loss = abs(mae.get("max_adverse_excursion_pct", 0) or 0)
        if mae_loss >= max_loss_plan:
            invalidation_triggered = True
            invalidation_reason = f"max_loss_breach:{mae_loss:.1f}%>={max_loss_plan}%"

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
        "max_adverse_excursion_pct": mae.get("max_adverse_excursion_pct"),
        "max_gain_before_loss_pct": mae.get("max_gain_before_loss_pct"),
        "is_fake_winner": mae.get("is_fake_winner", False),
        "excess_return_t5": excess_t5, "excess_return_t20": excess_t20, "excess_return_t60": excess_t60,
        "invalidation_triggered": invalidation_triggered,
        "invalidation_reason": invalidation_reason,
        "max_loss_plan": max_loss_plan,
        "error_type": "", "review_note": "",
        "created_at": created_at,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "safety": dict(DEFAULT_OUTCOME_SAFETY),
    }
