# allowlist: forbidden-token-definition
"""Replay Report — summary statistics from replay window"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone


def build_replay_report(replay_window_result: dict) -> dict:
    """Build summary report from replay window results."""
    results = replay_window_result.get("results", [])
    all_tickers = {}
    for day_result in results:
        for r in day_result.get("results", []):
            t = r.get("ticker")
            d = r.get("result", {}).get("decision", "UNKNOWN")
            if t:
                all_tickers.setdefault(t, []).append(d)
    total_days = len(results)
    seed = f"replay_report|{total_days}|{len(all_tickers)}"
    report_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "report_version": "REPLAY_REPORT_V10", "mode": "HISTORICAL_REPLAY_ONLY",
        "report_id": report_id, "created_at": created_at,
        "total_days": total_days, "tickers_tracked": len(all_tickers),
        "ticker_decisions": all_tickers,
        "real_trade_allowed": False, "broker_order_allowed": False,
    }
