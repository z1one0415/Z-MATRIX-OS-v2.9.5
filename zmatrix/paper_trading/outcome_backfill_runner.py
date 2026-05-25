"""Outcome Backfill Runner v1.0 — 基于本地价格历史的真实回填"""
from __future__ import annotations
from datetime import datetime, timedelta

def _find_price_on_date(bars: list[dict], target_date: str) -> float | None:
    for b in bars:
        d = b.get("date", "")[:10]
        if len(d) >= 10 and d[:10] == target_date[:10]:
            try: return float(b.get("adj_close", b.get("close", 0)))
            except: return None
    return None

def _calc_return(entry_price: float, exit_price: float) -> float | None:
    if entry_price and exit_price and entry_price > 0:
        return round((exit_price / entry_price - 1) * 100, 2)
    return None

def _calc_max_drawdown(bars: list[dict], entry_idx: int, window: int) -> float | None:
    segment = bars[entry_idx:entry_idx+window]
    if len(segment) < 2: return None
    peak = entry_price = None
    try: entry_price = float(segment[0].get("adj_close", segment[0].get("close", 0)))
    except: return None
    if not entry_price: return None
    peak = entry_price; mdd = 0.0
    for b in segment[1:]:
        try:
            p = float(b.get("adj_close", b.get("close", 0)))
            peak = max(peak, p)
            dd = (peak - p) / peak * 100
            mdd = max(mdd, dd)
        except: continue
    return round(mdd, 2)

def calculate_outcome_for_entry(paper_entry: dict, price_bars: list[dict]) -> dict:
    ticker = paper_entry.get("ticker", "")
    entry_date = paper_entry.get("entry_date", "")
    entry_price = paper_entry.get("entry_price", 0)

    bars = [b for b in price_bars if b.get("ticker", "").strip() == ticker or not ticker]
    bars_sorted = sorted(bars, key=lambda x: x.get("date", ""))

    if not bars_sorted or entry_price <= 0:
        return {"paper_id": paper_entry.get("paper_id",""), "ticker": ticker, "entry_date": entry_date,
                "actual_return_t5": None, "actual_return_t20": None, "actual_return_t60": None,
                "max_drawdown_t20": None, "max_drawdown_t60": None,
                "outcome_status": "INSUFFICIENT_DATA", "real_z9_write_allowed": False}

    entry_idx = None
    for i, b in enumerate(bars_sorted):
        if b.get("date", "")[:10] >= entry_date[:10]:
            entry_idx = i; break
    if entry_idx is None: entry_idx = 0

    entry_close = entry_price
    try: entry_close = float(bars_sorted[entry_idx].get("adj_close", bars_sorted[entry_idx].get("close", entry_price)))
    except: pass

    horizons = {"T5": 5, "T20": 20, "T60": 60}
    returns = {}; drawdowns = {}

    for h, days in horizons.items():
        target_idx = entry_idx + days
        if target_idx < len(bars_sorted):
            try:
                exit_p = float(bars_sorted[target_idx].get("adj_close", bars_sorted[target_idx].get("close", 0)))
                returns[h] = _calc_return(entry_close, exit_p)
            except: returns[h] = None
        else: returns[h] = None

    for h, days in [("T20", 20), ("T60", 60)]:
        if entry_idx + days <= len(bars_sorted):
            drawdowns[h] = _calc_max_drawdown(bars_sorted, entry_idx, days)
        else: drawdowns[h] = None

    return {
        "paper_id": paper_entry.get("paper_id", ""),
        "ticker": ticker, "entry_date": entry_date,
        "actual_return_t5": returns.get("T5"),
        "actual_return_t20": returns.get("T20"),
        "actual_return_t60": returns.get("T60"),
        "max_drawdown_t20": drawdowns.get("T20"),
        "max_drawdown_t60": drawdowns.get("T60"),
        "outcome_status": "READY" if any(returns.values()) else "INSUFFICIENT_DATA",
        "real_z9_write_allowed": False,
    }
