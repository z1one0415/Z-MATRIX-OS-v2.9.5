"""Batch Runner — batch outcome backfill with skip-existing"""
from __future__ import annotations
from datetime import datetime, timezone
from zmatrix.paper_outcome.outcome_backfill_runner import run_outcome_backfill

def run_outcome_batch(paper_entries: list[dict], price_paths: dict[str, list[float]]) -> dict:
    """Run outcome backfill for multiple paper entries."""
    results = []
    ok, fail, skip = 0, 0, 0
    for entry in paper_entries:
        tid = entry.get("paper_id", "")
        ticker = entry.get("ticker", "")
        path = price_paths.get(ticker)
        r = run_outcome_backfill(paper_entry=entry, price_path=path)
        results.append(r)
        if r["outcome_status"] == "READY":
            ok += 1
        elif r["outcome_status"] == "INSUFFICIENT_DATA":
            fail += 1
        else:
            skip += 1
    return {
        "batch_version": "OUTCOME_BATCH_V10",
        "executed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": len(paper_entries), "ok": ok, "fail": fail, "skip": skip,
        "results": results,
        "real_trade_allowed": False, "broker_order_allowed": False,
    }
