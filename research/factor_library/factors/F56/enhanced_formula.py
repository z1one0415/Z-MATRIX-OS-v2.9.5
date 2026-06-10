"""Enhanced formula for F56 MONEY_FLOW_STRENGTH.
Primitives: turnover_rate, vol_ratio
Enhanced with vol_ratio and turnover proxy — captures flow intensity
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
    """Compute F56 MONEY_FLOW_STRENGTH (enhanced variant)."""
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 5:
            scores[ticker] = 0.0; continue
        total_mf,total_vol=0.0,0.0
        for b in bars[-5:]:
            rng=b["high"]-b["low"]; clv=(b["close"]-b["low"])/max(rng,0.0001)
            total_mf+=clv*b["volume"]; total_vol+=b["volume"]
        base=total_mf/max(total_vol,1)
        # turnover_rate proxy, vol_ratio
        avg_vol=sum(b["volume"] for b in bars[-20:])/20 if len(bars)>=20 else total_vol
        vol_ratio=total_vol/max(avg_vol,1)
        scores[ticker]=round(base+vol_ratio*0.01,6)
    return scores

def rank_and_bucket(scores):
    """Rank scores descending (1=best) and assign bucket 1-5."""
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {t:{"score":round(s,6),"rank":i+1,"bucket":min(5,max(1,math.ceil((i+1)*5/n)))} for i,(t,s) in enumerate(items)}
