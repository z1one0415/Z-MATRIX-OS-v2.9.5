"""Executable formula for F54 CROWDING_RISK.

Factor type: PRICE_VOLUME_ATTENTION
Formula: volume_zscore+high_volume_day_count
Source: data/price_bars
Signal role: FACTOR_SIGNAL_ONLY

DO NOT use forward_return or outcome labels in computation.
DO NOT output alpha_signal, trade_signal, position, order.
"""
import csv, math
from pathlib import Path
from datetime import date

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
SIGNAL_ROLE = "FACTOR_SIGNAL_ONLY"
FACTOR_ID = "F54"

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
                    "date": d, "open": float(row["open"]), "high": float(row["high"]),
                    "low": float(row["low"]), "close": float(row["close"]),
                    "volume": int(row["volume"])
                })
    for t in data:
        data[t].sort(key=lambda x: x["date"])
    return data

def compute_signal(input_prices, rebalance_date):
    """Compute F54 CROWDING_RISK signal scores.

    Formula: volume_zscore+high_volume_day_count
    Source: data/price_bars

    Returns: dict of ticker -> signal_score (float)
    """
    # This is a placeholder - actual factor formula implementation
    # should use the pre-rebalance price data to compute scores.
    # For reproducible signal-ready classification, this function
    # must be able to reproduce the signal_scores.csv from source data.
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 5:
            scores[ticker] = 0.0
            continue
        # Factor-specific computation goes here
        scores[ticker] = 0.0  # Replace with actual formula
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

def main(tickers, rebalance_date=None):
    """Generate signal scores for given tickers at rebalance_date."""
    if rebalance_date is None:
        rebalance_date = date(2026, 5, 6)
    prices = load_pre_rebalance_prices(rebalance_date, set(tickers))
    raw_scores = compute_signal(prices, rebalance_date)
    return rank_and_bucket(raw_scores)
