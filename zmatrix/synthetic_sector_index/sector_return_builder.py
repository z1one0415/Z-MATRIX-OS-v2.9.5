# allowlist: forbidden-token-definition
from __future__ import annotations
import csv
from pathlib import Path
from collections import defaultdict
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY, MIN_ACTIVE_MEMBERS, MIN_ACTIVE_MEMBER_RATIO

def _tf(x):
    try:
        if x in (None,""): return None
        return float(x)
    except: return None

def _load_ticker_bars(ticker, data_root):
    bare = str(ticker).split(".")[0].zfill(6)
    p = Path(data_root)/"data"/"price_bars"/f"{bare}.csv"
    if not p.exists(): return None,{}
    closes = {}
    with open(p,"r",encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = str(r.get("trade_date") or r.get("date","")).replace("-","")[:8]; c = _tf(r.get("close"))
            if d and c is not None: closes[d] = c
    return bare, closes

def build_sector_daily_returns(*, sector_mapping: dict, data_root=".") -> dict:
    members = defaultdict(list)
    for tk,m in (sector_mapping or {}).items():
        if m.get("sector"): members[m["sector"]].append(tk)
    # Preload all price bars
    print(f"  Loading price bars for {sum(len(v) for v in members.values())} tickers...", flush=True)
    all_bars = {}
    missing = []
    for sector, tickers in members.items():
        for tk in tickers:
            _, bars = _load_ticker_bars(tk, data_root)
            if bars: all_bars[tk] = bars
            else: missing.append(tk)
    print(f"  Loaded {len(all_bars)} tickers, {len(set(missing))} missing", flush=True)
    # Compute daily returns per sector
    sd = {}
    for sector, tickers in members.items():
        dm = defaultdict(list)
        for tk in tickers:
            bars = all_bars.get(tk)
            if not bars: continue
            dates = sorted(bars.keys())
            for i in range(1,len(dates)):
                prev = bars[dates[i-1]]; cur = bars[dates[i]]
                if prev and cur and prev>0: dm[dates[i]].append((cur-prev)/prev*100)
        mc = len(tickers); rows = []
        for d in sorted(dm.keys()):
            rets = dm[d]; active = len(rets); ratio = active/mc if mc else 0
            q = "INSUFFICIENT_MEMBERS" if active<MIN_ACTIVE_MEMBERS else "LOW_COVERAGE" if ratio<MIN_ACTIVE_MEMBER_RATIO else "READY"
            rows.append({"sector":sector,"trade_date":d,"sector_return_1d":sum(rets)/len(rets) if rets else None,"member_count":mc,"active_member_count":active,"active_member_ratio":ratio,"data_quality_status":q,"synthetic_sector_index":True,"production_index_allowed":False})
        sd[sector] = rows
    return {"builder_version":"V3511_SECTOR_DAILY_RETURN_BUILDER_V10","sector_count":len(sd),"missing_price_file_count":len(set(missing)),"missing_price_files_sample":sorted(set(missing))[:100],"sector_daily_returns":sd,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
