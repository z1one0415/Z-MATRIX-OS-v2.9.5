"""Enhanced formula for F04 RESIDUAL_MOMENTUM.
Primitives: mom_20d, mom_60d, ma60_dev
Adaptive lookback: uses available data when <60 bars instead of returning 0.
Signal role: FACTOR_SIGNAL_ONLY — enhanced variant, does not replace original.
"""
import csv, math
from datetime import date
from pathlib import Path

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
SIGNAL_ROLE = "FACTOR_SIGNAL_ONLY"

def load_pre_rebalance_prices(rebalance_date, tickers=None):
    if tickers is None: tickers = set()
    data = {}
    with open(PRICE_BARS) as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d < rebalance_date:
                t = row["ticker"]
                if tickers and t not in tickers: continue
                if t not in data: data[t] = []
                data[t].append({"date":d,"open":float(row["open"]),"high":float(row["high"]),
                                 "low":float(row["low"]),"close":float(row["close"]),"volume":int(row["volume"])})
    for t in data: data[t].sort(key=lambda x: x["date"])
    return data

def compute_signal(input_prices, rebalance_date):
    """Compute F04 RESIDUAL_MOMENTUM (enhanced variant with adaptive lookback)."""
    scores = {}
    for ticker, bars in input_prices.items():
        n = len(bars)
        if n < 20:
            scores[ticker] = 0.0
            continue
        
        # mom_20d: use last 20 bars or max available
        lookback_20 = min(20, n - 1)
        mom_20d = (bars[-1]["close"] - bars[-lookback_20]["close"]) / max(bars[-lookback_20]["close"], 0.0001)
        
        # mom_60d: use last 60 bars or max available
        lookback_60 = min(60, n - 1)
        mom_60d = (bars[-1]["close"] - bars[-lookback_60]["close"]) / max(bars[-lookback_60]["close"], 0.0001)
        
        # ma60_dev: use min(60, n) moving average
        lookback_ma = min(60, n)
        ma = sum(b["close"] for b in bars[-lookback_ma:]) / lookback_ma
        ma_dev = (bars[-1]["close"] - ma) / max(ma, 0.001)
        
        # Trend alignment bonus
        positive_count = sum(1 for i in range(max(0,n-20), n) if bars[i]["close"] > bars[max(0,i-1)]["close"])
        trend_strength = (positive_count - (min(20,n)-positive_count)) / min(20,n)
        
        scores[ticker] = round(mom_20d * 0.4 + mom_60d * 0.3 + ma_dev * 0.2 + trend_strength * 0.1, 6)
    return scores

def rank_and_bucket(scores):
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {t:{"score":round(s,6),"rank":i+1,"bucket":min(5,max(1,math.ceil((i+1)*5/n)))} for i,(t,s) in enumerate(items)}
