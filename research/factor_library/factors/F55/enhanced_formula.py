"""Enhanced formula for F55 SENTIMENT_DECAY.
Primitives: attention_decay_alignment
Enhanced with decay_strength factor — penalizes sharp attention drops
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
    """Compute F55 SENTIMENT_DECAY (enhanced variant)."""
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 20:
            scores[ticker] = 0.0; continue
        ratios=[]
        for i in range(5,len(bars)):
            r5=sum(b["volume"] for b in bars[i-5:i])/5
            r20=sum(b["volume"] for b in bars[max(0,i-20):i])/max(1,min(20,i))
            ratios.append(r5/max(r20,1))
        peak=max(ratios) if ratios else 1.0
        current=ratios[-1] if ratios else 1.0
        # Enhanced: decay_strength from how far from peak
        decay=-(current-peak)
        decay_strength=abs(current-peak)/max(peak,0.001)
        scores[ticker]=round(decay*(1+decay_strength*0.5),6)
    return scores

def rank_and_bucket(scores):
    """Rank scores descending (1=best) and assign bucket 1-5."""
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {t:{"score":round(s,6),"rank":i+1,"bucket":min(5,max(1,math.ceil((i+1)*5/n)))} for i,(t,s) in enumerate(items)}
