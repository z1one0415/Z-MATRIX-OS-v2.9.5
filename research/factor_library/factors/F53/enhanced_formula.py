"""Enhanced formula for F53 ATTENTION_SPIKE.
Primitives: vol_climax, vol_ratio
Enhanced with vol_ratio and vol_climax — attention spike detection
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
    """Compute F53 ATTENTION_SPIKE (enhanced variant)."""
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 20:
            scores[ticker] = 0.0; continue
        vol_5d=sum(b["volume"] for b in bars[-5:])/5
        vol_20d=sum(b["volume"] for b in bars[-20:])/20
        ret_5d=(bars[-1]["close"]-bars[-5]["close"])/max(bars[-5]["close"],0.0001)
        vol_ratio=vol_5d/max(vol_20d,1)
        # vol_climax: look for volume spike above 2 std
        vols=[b["volume"] for b in bars[-20:]]; mv=sum(vols)/len(vols)
        sv=(sum((v-mv)**2 for v in vols)/len(vols))**0.5
        climax=1.0 if vols[-1]>mv+2*sv else 0.0
        scores[ticker]=round(vol_ratio*abs(ret_5d)+climax*0.5,6)
    return scores

def rank_and_bucket(scores):
    """Rank scores descending (1=best) and assign bucket 1-5."""
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {t:{"score":round(s,6),"rank":i+1,"bucket":min(5,max(1,math.ceil((i+1)*5/n)))} for i,(t,s) in enumerate(items)}
