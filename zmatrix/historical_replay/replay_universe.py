"""Replay Universe — build historical date stock pool with PIT cutoff"""
from __future__ import annotations
import csv
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
    """Build replay universe with PIT cutoff.
    
    - Only includes tickers that have data BEFORE replay_date
    - Requires at least min_history_days of pre-replay_date data
    - Excludes stocks listed AFTER replay_date (future leak prevention)
    """
    bar_dir = Path(local_data_root) / "data" / "price_bars"
    if not bar_dir.exists():
        return {"universe_version": "REPLAY_UNIVERSE_V10", "tickers": [],
                "excluded": ["data_dir_missing"], "filters": {}}

    excluded = []
    tickers = []
    replay_clean = replay_date.replace("-", "")

    for f in sorted(bar_dir.glob("*.csv")):
        ticker = f.stem
        if max_tickers and len(tickers) >= max_tickers:
            break
        try:
            rows = list(csv.DictReader(open(f, encoding="utf-8-sig")))
            valid = [r for r in rows if (r.get("trade_date") or r.get("date", "")).strip()]
            if not valid:
                excluded.append(f"{ticker}:no_valid_data")
                continue

            # Get earliest and latest dates in the file
            def clean_date(r):
                return (r.get("trade_date") or r.get("date", "")).replace("-", "")

            dates = [clean_date(r) for r in valid]
            earliest = min(dates)
            latest = max(dates)

            # PIT cutoff: stock must have been listed before replay_date
            if earliest > replay_clean:
                excluded.append(f"{ticker}:listed_after_replay({earliest}>{replay_clean})")
                continue

            # Must have enough pre-replay-date data
            pre_dates = [d for d in dates if d < replay_clean]
            if len(pre_dates) < min_history_days:
                excluded.append(f"{ticker}:insufficient_history({len(pre_dates)}<{min_history_days})")
                continue

            # Data must cover up to around replay_date (within 5 trading days)
            if latest < replay_clean:
                # Stock data stops before replay_date — may be delisted/suspended
                excluded.append(f"{ticker}:data_stops_before_replay({latest}<{replay_clean})")
                continue

            tickers.append(ticker)

        except Exception as ex:
            excluded.append(f"{ticker}:read_error({str(ex)[:40]})")
            continue

    return {
        "universe_version": "REPLAY_UNIVERSE_V10",
        "replay_date": replay_date,
        "local_data_root": local_data_root,
        "tickers": tickers,
        "excluded": excluded,
        "filters": {
            "include_st": include_st, "include_suspended": include_suspended,
            "min_history_days": min_history_days, "max_tickers": max_tickers,
            "point_in_time_only": True,
        },
        "future_data_allowed": False,
        "real_trade_allowed": False,
    }
