"""Replay Window — multi-date rolling replay with WEEKLY default"""
from __future__ import annotations
import hashlib
from datetime import datetime, timedelta, timezone

from zmatrix.historical_replay.replay_engine import run_single_day_replay

_HISTORICAL_REPLAY_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "runtime_enabled": False, "future_data_allowed": False,
}


def run_replay_window(*, start_date: str, end_date: str,
                        local_data_root: str, frequency: str = "WEEKLY",
                        max_tickers: int | None = None) -> dict:
    """Run replay over a date window, default WEEKLY."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=7) if frequency == "WEEKLY" else timedelta(days=1)
    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime("%Y-%m-%d"))
        current += step
    results = []
    for d in dates:
        r = run_single_day_replay(
            replay_date=d, local_data_root=local_data_root,
            max_tickers=max_tickers,
        )
        results.append(r)
    seed = f"{start_date}|{end_date}|{len(results)}"
    window_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "window_version": "REPLAY_WINDOW_V10", "mode": "HISTORICAL_REPLAY_ONLY",
        "window_id": window_id, "start_date": start_date, "end_date": end_date,
        "frequency": frequency, "created_at": created_at,
        "dates_covered": len(dates), "results": results,
        "real_trade_allowed": False, "broker_order_allowed": False,
        "safety": dict(_HISTORICAL_REPLAY_SAFETY),
    }
