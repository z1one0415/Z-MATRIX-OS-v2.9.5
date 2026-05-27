from __future__ import annotations
import json, csv
from pathlib import Path
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

def _clean_date(x): return str(x or "").replace("-", "").strip()
def _to_float(x):
    try:
        if x in (None, ""): return None
        return float(x)
    except Exception: return None
def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs)/len(xs) if xs else None
def _return_pct(a,b):
    if a is None or b in (None,0): return None
    return (a-b)/b*100

def load_entry_history(*, ticker: str, entry_date: str, data_root: str = ".", lookback_days: int = 80) -> list[dict]:
    bare = str(ticker).split(".")[0]; path = Path(data_root)/"data"/"price_bars"/f"{bare}.csv"
    if not path.exists(): return []
    entry = _clean_date(entry_date); rows = []
    with open(path,"r",encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            d = _clean_date(row.get("trade_date") or row.get("date"))
            if not d or d > entry: continue
            close = _to_float(row.get("close")); volume = _to_float(row.get("volume") or row.get("vol"))
            if close is None: continue
            rows.append({"trade_date":d,"close":close,"volume":volume})
    rows = sorted(rows, key=lambda x: x["trade_date"])
    return rows[-lookback_days:]

def build_entry_features(*, sample: dict, data_root: str = ".") -> dict:
    hist = load_entry_history(ticker=sample.get("ticker"), entry_date=sample.get("entry_date"), data_root=data_root, lookback_days=80)
    if len(hist) < 20: return {"feature_status":"INSUFFICIENT_HISTORY","paper_id":sample.get("paper_id"),"ticker":sample.get("ticker"),"features":{},"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
    closes = [x["close"] for x in hist]; vols = [x["volume"] for x in hist if x.get("volume") is not None]
    c0=closes[-1]; c5=closes[-6] if len(closes)>=6 else None; c20=closes[-21] if len(closes)>=21 else None; c60=closes[-61] if len(closes)>=61 else None
    ma20=_mean(closes[-20:]); ma60=_mean(closes[-60:]) if len(closes)>=60 else None
    high20=max(closes[-20:]); low20=min(closes[-20:])
    daily_abs=[]
    for i in range(1, len(closes[-21:])):
        prev=closes[-21:][i-1]; cur=closes[-21:][i]
        if prev: daily_abs.append(abs((cur-prev)/prev*100))
    vol5=_mean(vols[-5:]) if len(vols)>=5 else None; vol20=_mean(vols[-20:]) if len(vols)>=20 else None
    brd = sample.get("source_brd_result",{}) or {}; raw = brd.get("source_raw",{}) or {}; b_matrix = raw.get("b_matrix") or brd.get("b_matrix") or {}
    features = {"return_5d":_return_pct(c0,c5),"return_20d":_return_pct(c0,c20),"return_60d":_return_pct(c0,c60),"distance_to_ma20":_return_pct(c0,ma20),"distance_to_ma60":_return_pct(c0,ma60),"price_above_ma20":c0>ma20 if ma20 is not None else None,"price_above_ma60":c0>ma60 if ma60 is not None else None,"drawdown_from_20d_high":_return_pct(c0,high20),"bounce_from_20d_low":_return_pct(c0,low20),"volume_ratio_5_20":vol5/vol20 if vol5 is not None and vol20 not in (None,0) else None,"volatility_20d":_mean(daily_abs),"b_score":b_matrix.get("b_score"),"quality_score":b_matrix.get("quality_score"),"growth_score":b_matrix.get("growth_score"),"valuation_score":b_matrix.get("valuation_score"),"role_cap":b_matrix.get("role_cap"),"valuation_data_status":b_matrix.get("valuation_data_status")}
    return {"feature_version":"V355_ENTRY_FEATURES_V10","feature_status":"READY","paper_id":sample.get("paper_id"),"ticker":sample.get("ticker"),"entry_date":sample.get("entry_date"),"features":features,"history_count":len(hist),"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
