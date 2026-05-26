"""Replay Universe — build historical date stock pool from local data"""
from __future__ import annotations
import json
from pathlib import Path

_HISTORICAL_REPLAY_SAFETY = {
    "real_trade_allowed": False, "broker_order_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "runtime_enabled": False, "future_data_allowed": False,
}


def build_replay_universe(*, replay_date: str, local_data_root: str,
                           include_st: bool = False, include_suspended: bool = False,
                           min_history_days: int = 120,
                           max_tickers: int | None = None) -> dict:
    """Build replay universe for a given historical date."""
    bar_dir = Path(local_data_root) / "data" / "price_bars"
    if not bar_dir.exists():
        return {"universe_version": "REPLAY_UNIVERSE_V10", "tickers": [],
                "excluded": ["data_dir_missing"], "filters": {}}
    excluded = []
    tickers = []
    for f in sorted(bar_dir.glob("*.csv")):
        ticker = f.stem
        if max_tickers and len(tickers) >= max_tickers:
            break
        try:
            rows = f.read_text(encoding="utf-8-sig").strip().split("\n")
            if len(rows) < min_history_days + 1:
                excluded.append(f"{ticker}:short_history({len(rows)-1})")
                continue
        except Exception:
            excluded.append(f"{ticker}:read_error")
            continue
        tickers.append(ticker)
    return {
        "universe_version": "REPLAY_UNIVERSE_V10",
        "replay_date": replay_date, "local_data_root": local_data_root,
        "tickers": tickers, "excluded": excluded,
        "filters": {"include_st": include_st, "include_suspended": include_suspended,
                     "min_history_days": min_history_days, "max_tickers": max_tickers},
        "future_data_allowed": False, "real_trade_allowed": False,
    }
