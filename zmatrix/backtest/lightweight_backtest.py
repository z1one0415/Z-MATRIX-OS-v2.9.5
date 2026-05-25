"""Lightweight Backtest v1.0 — 基于 paper entries 的角色回测"""
from __future__ import annotations
from datetime import datetime

def calc_return(entry_price, exit_price):
    if entry_price and exit_price and entry_price > 0:
        return round((exit_price / entry_price - 1) * 100, 2)
    return None

def calc_max_drawdown(prices: list[float]) -> float | None:
    if len(prices) < 2: return None
    peak = prices[0]; mdd = 0.0
    for p in prices[1:]:
        peak = max(peak, p)
        dd = (peak - p) / peak * 100
        mdd = max(mdd, dd)
    return round(mdd, 2)

def calc_win_rate(returns: list[float]) -> float:
    if not returns: return 0.0
    return round(sum(1 for r in returns if r > 0) / len(returns) * 100, 1)

def calc_avg_return(returns: list[float]) -> float:
    if not returns: return 0.0
    return round(sum(returns) / len(returns), 2)

def run_lightweight_role_backtest(paper_entries: list[dict], price_bars_by_ticker: dict[str, list[dict]]) -> dict:
    roles = {}
    for e in paper_entries:
        role = e.get("role", "UNKNOWN")
        if role not in roles: roles[role] = []
        roles[role].append(e)

    results = {"A_LONG_CORE": {}, "B_MID_ROTATION": {}, "C_SHORT_EVENT": {}, "ALL": {}}
    all_t5, all_t20, all_t60 = [], [], []

    for role, entries in roles.items():
        if role not in results: continue
        t5s, t20s, t60s = [], [], []
        for e in entries:
            bars = price_bars_by_ticker.get(e.get("ticker",""), [])
            if not bars or not e.get("entry_price"): continue
            idx = 0; ep = float(e.get("entry_price",0))
            for i, b in enumerate(bars):
                if b.get("date","")[:10] >= e.get("entry_date","")[:10]: idx = i; break
            if idx + 5 < len(bars):
                try:
                    ex = float(bars[idx+5].get("adj_close", bars[idx+5].get("close",0)))
                    if ep > 0: t5s.append(round((ex/ep - 1)*100,2))
                except: pass
            if idx + 20 < len(bars):
                try:
                    ex = float(bars[idx+20].get("adj_close", bars[idx+20].get("close",0)))
                    if ep > 0: t20s.append(round((ex/ep - 1)*100,2))
                except: pass
        results[role] = {
            "count": len(entries), "win_rate_t5": calc_win_rate(t5s),
            "avg_return_t5": calc_avg_return(t5s) if t5s else None,
            "win_rate_t20": calc_win_rate(t20s) if t20s else None,
            "avg_return_t20": calc_avg_return(t20s) if t20s else None,
        }
        all_t5.extend(t5s); all_t20.extend(t20s)

    results["ALL"] = {
        "count": len(paper_entries),
        "win_rate_t5": calc_win_rate(all_t5),
        "avg_return_t5": calc_avg_return(all_t5) if all_t5 else None,
        "win_rate_t20": calc_win_rate(all_t20),
        "avg_return_t20": calc_avg_return(all_t20) if all_t20 else None,
    }

    return results
