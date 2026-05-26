"""Outcome Summary Report — aggregate stats"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

def build_outcome_summary(outcome_results: list[dict]) -> dict:
    """Build summary report from batch outcome results."""
    ready = [r for r in outcome_results if r.get("outcome_status") == "READY"]
    if not ready:
        return {"status": "NO_DATA", "total": 0}
    t20_returns = [r["actual_return_t20"] for r in ready if r.get("actual_return_t20") is not None]
    t5_returns = [r["actual_return_t5"] for r in ready if r.get("actual_return_t5") is not None]
    wins_t20 = [r for r in t20_returns if r > 0]
    seed = f"outcome_summary|{len(ready)}"
    report_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    return {
        "report_version": "OUTCOME_SUMMARY_V10",
        "report_id": report_id,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_ready": len(ready),
        "avg_return_t5": round(sum(t5_returns)/len(t5_returns), 2) if t5_returns else None,
        "avg_return_t20": round(sum(t20_returns)/len(t20_returns), 2) if t20_returns else None,
        "win_rate_t20": round(len(wins_t20)/len(t20_returns)*100, 1) if t20_returns else None,
        "real_trade_allowed": False, "broker_order_allowed": False,
    }
