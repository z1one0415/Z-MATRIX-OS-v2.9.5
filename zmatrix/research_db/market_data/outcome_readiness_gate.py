"""Phase 3-B: Outcome Readiness Gate — batch check + summary."""
from __future__ import annotations
from zmatrix.research_db.market_data.outcome_schema import OutcomeHorizonResult

def check_outcome_ready(engine, ticker: str, observation_date: str, horizon: str) -> bool:
    r = engine.evaluate_horizon(ticker, observation_date, horizon)
    return r.readiness_status == "READY"

def batch_check_outcome_ready(engine, requests: list[dict]) -> list[OutcomeHorizonResult]:
    return engine.evaluate_many(requests)

def summarize_readiness(results: list[OutcomeHorizonResult]) -> dict:
    total = len(results)
    ready = sum(1 for r in results if r.readiness_status == "READY")
    insufficient = sum(1 for r in results if r.readiness_status == "INSUFFICIENT_FORWARD_DAYS")
    missing_entry = sum(1 for r in results if r.readiness_status == "MISSING_ENTRY_BAR")
    missing_exit = sum(1 for r in results if r.readiness_status == "MISSING_EXIT_BAR")
    suspended = sum(1 for r in results if "SUSPENDED" in r.readiness_status)
    fallback = sum(1 for r in results if r.fallback_used)
    blocked = total - ready
    return {
        "total": total, "ready_count": ready, "blocked_count": blocked,
        "insufficient_forward_days_count": insufficient, "missing_entry_bar_count": missing_entry,
        "missing_exit_bar_count": missing_exit, "suspended_count": suspended,
        "fallback_used_count": fallback, "production_allowed": False,
    }
