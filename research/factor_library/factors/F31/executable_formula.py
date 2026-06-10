"""Executable formula for F31 DOWNSIDE_TAIL_RISK.

Factor type: PRICE_VOLUME_RISK
Formula: -max_drawdown_20d
Source: data/price_bars
Signal role: FACTOR_SIGNAL_ONLY
"""
import csv, math
from datetime import date
from pathlib import Path

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
SIGNAL_ROLE = "FACTOR_SIGNAL_ONLY"


def load_pre_rebalance_prices(rebalance_date, tickers=None):
    """Load OHLCV data strictly BEFORE rebalance_date."""
    if tickers is None:
        tickers = set()
    data = {}
    with open(PRICE_BARS) as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d < rebalance_date:
                t = row["ticker"]
                if tickers and t not in tickers:
                    continue
                if t not in data:
                    data[t] = []
                data[t].append({
                    "date": d, "open": float(row["open"]),
                    "high": float(row["high"]), "low": float(row["low"]),
                    "close": float(row["close"]), "volume": int(row["volume"])
                })
    for t in data:
        data[t].sort(key=lambda x: x["date"])
    return data


def compute_signal(input_prices, rebalance_date):
    """Compute F31 DOWNSIDE_TAIL_RISK signal scores.

    Formula: -max_drawdown_20d
    Source: data/price_bars
    """
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 5:
            scores[ticker] = 0.0
            continue
        prices = [b["close"] for b in bars]
        peak = prices[0]; max_dd = 0.0
        for p in prices:
            if p > peak: peak = p
            dd = (p - peak) / max(peak, 0.0001)
            if dd < max_dd: max_dd = dd
        scores[ticker] = round(-max_dd, 6)
    return scores


def rank_and_bucket(scores):
    """Rank scores descending (1=best) and assign bucket 1-5."""
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {
        t: {"score": round(s, 6), "rank": i + 1,
             "bucket": min(5, max(1, math.ceil((i + 1) * 5 / n)))}
        for i, (t, s) in enumerate(items)
    }
