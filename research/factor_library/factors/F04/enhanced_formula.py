"""Enhanced formula for F04 RESIDUAL_MOMENTUM.
Primitives: mom_20d, mom_60d, ma60_dev
Enhanced with mom_20d, mom_60d (momentum), ma60_dev (trend alignment)
Signal role: FACTOR_SIGNAL_ONLY — enhanced variant, does not replace original.
"F7 canonical baseline unchanged."
"""
import csv, math
from datetime import date
from pathlib import Path

PRICE_BARS = Path("data/price_bars/daily_bars.csv")
SIGNAL_ROLE = "FACTOR_SIGNAL_ONLY"

def load_pre_rebalance_prices(rebalance_date, tickers=None):
    """Load OHLCV data strictly BEFORE rebalance_date."""
    if tickers is None: tickers = set()
    data = {}
    with open(PRICE_BARS) as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d < rebalance_date:
                t = row["ticker"]
                if tickers and t not in tickers: continue
                if t not in data: data[t] = []
                data[t].append({"date":d,"open":float(row["open"]),"high":float(row["high"]),"low":float(row["low"]),"close":float(row["close"]),"volume":int(row["volume"])})
    for t in data: data[t].sort(key=lambda x: x["date"])
    return data

def compute_signal(input_prices, rebalance_date):
    """Compute F04 RESIDUAL_MOMENTUM (enhanced variant)."""
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 60:
            scores[ticker] = 0.0; continue
        mom_20d = (bars[-1]["close"] - bars[-20]["close"]) / max(bars[-20]["close"], 0.0001)
        mom_60d = (bars[-1]["close"] - bars[-60]["close"]) / max(bars[-60]["close"], 0.0001)
        ma60 = sum(b["close"] for b in bars[-60:]) / 60
        ma60_dev = (bars[-1]["close"] - ma60) / max(ma60, 0.001)
        # Enhanced: add momentum + trend alignment
        trend_alignment = 1.0 if (mom_20d > 0 and mom_60d > 0 and ma60_dev > 0) else -1.0 if (mom_20d < 0 and mom_60d < 0 and ma60_dev < 0) else 0.0
        scores[ticker] = round(mom_20d + mom_60d * 0.5 + ma60_dev * 0.3 + trend_alignment * 0.01, 6)
    return scores

def rank_and_bucket(scores):
    """Rank scores descending (1=best) and assign bucket 1-5."""
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {t:{"score":round(s,6),"rank":i+1,"bucket":min(5,max(1,math.ceil((i+1)*5/n)))} for i,(t,s) in enumerate(items)}
