"""Enhanced formula for F30 VOLUME_PRICE_CONFIRMATION.
Primitives: strengthened_volume_correlation
Enhanced with up_volume_ratio and down_volume_pressure — strengthens signal quality
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
    """Compute F30 VOLUME_PRICE_CONFIRMATION (enhanced variant)."""
    scores = {}
    for ticker, bars in input_prices.items():
        if len(bars) < 20:
            scores[ticker] = 0.0; continue
        rets=[(bars[i]["close"]-bars[i-1]["close"])/max(bars[i-1]["close"],0.0001) for i in range(1,len(bars))]
        vc=[(bars[i]["volume"]-bars[i-1]["volume"])/max(bars[i-1]["volume"],1) for i in range(1,len(bars))]
        n=min(len(rets),len(vc))
        if n<5: scores[ticker]=0.0; continue
        r,v_=rets[:n],vc[:n]; mr=sum(r)/n; mv_=sum(v_)/n
        cov=sum((r[i]-mr)*(v_[i]-mv_) for i in range(n))/n
        sr=(sum((x-mr)**2 for x in r)/n)**0.5; sv=(sum((x-mv_)**2 for x in v_)/n)**0.5
        corr=cov/max(sr*sv,0.0001) if sr>0.0001 and sv>0.0001 else 0
        # Enhanced: add up_day_volume_ratio + down_day_volume_pressure
        up_days=[rets[i] for i in range(n) if rets[i]>0 and vc[i]>(sum(vc)/n if sum(vc)/n!=0 else 0)]
        down_days=[abs(rets[i]) for i in range(n) if rets[i]<0 and vc[i]>(sum(vc)/n if sum(vc)/n!=0 else 0)]
        up_ratio=len(up_days)/max(n,1); down_pressure=sum(down_days)/max(n,1)
        scores[ticker]=round(corr+up_ratio*0.5-down_pressure*0.3,6)
    return scores

def rank_and_bucket(scores):
    """Rank scores descending (1=best) and assign bucket 1-5."""
    items = [(t, s) for t, s in scores.items()]
    items.sort(key=lambda x: -x[1])
    n = len(items)
    return {t:{"score":round(s,6),"rank":i+1,"bucket":min(5,max(1,math.ceil((i+1)*5/n)))} for i,(t,s) in enumerate(items)}
