from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def _to_float(x):
    try:
        if x in (None,""): return None
        return float(x)
    except: return None

def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs)/len(xs) if xs else None

def _build_index_features(index_bars: dict, entry_date: str):
    entry = entry_date.replace("-",""); closes = []; vols = []; dates = sorted(index_bars.keys())
    for d in dates:
        if d > entry: break
        b = index_bars[d]; closes.append(_to_float(b.get("close"))); vols.append(_to_float(b.get("volume")))
    if len(closes) < 20: return None
    c0 = closes[-1]; c5 = closes[-6] if len(closes)>=6 else None; c20 = closes[-21] if len(closes)>=21 else None; c60 = closes[-61] if len(closes)>=61 else None
    ma20 = _mean(closes[-20:]); ma60 = _mean(closes[-60:]) if len(closes)>=60 else None
    high20 = max(closes[-20:]); low20 = min(closes[-20:])
    d_abs = [abs((closes[i]-closes[i-1])/closes[i-1]*100) for i in range(max(1,len(closes)-20),len(closes)) if closes[i-1]>0]
    vol5 = _mean(vols[-5:]) if len(vols)>=5 else None; vol20 = _mean(vols[-20:]) if len(vols)>=20 else None
    return {"close":c0,"return_5d":(c0-c5)/c5*100 if c5 else None,"return_20d":(c0-c20)/c20*100 if c20 else None,"return_60d":(c0-c60)/c60*100 if c60 else None,"above_ma20":c0>ma20 if ma20 else None,"above_ma60":c0>ma60 if ma60 else None,"drawdown_20d":(c0-high20)/high20*100 if high20 else None,"volatility_20d":_mean(d_abs),"volume_ratio_5_20":vol5/vol20 if vol5 and vol20 else None}

def classify_market_regime(*, index_features: dict | None) -> dict:
    if index_features is None: return {"regime":"UNKNOWN_MARKET_REGIME","regime_data_status":"DATA_INSUFFICIENT","uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
    r20 = index_features.get("return_20d"); above20 = index_features.get("above_ma20"); above60 = index_features.get("above_ma60")
    vol = index_features.get("volatility_20d"); vr = index_features.get("volume_ratio_5_20")
    regimes = []
    if above20 and above60 and r20 is not None and r20 > 3: regimes.append("BULL_TREND")
    if above60 is False and r20 is not None and r20 < -5: regimes.append("BEAR_TREND")
    if r20 is not None and -5 <= r20 <= 5: regimes.append("RANGE_BOUND")
    if vr is not None and vr > 1.2: regimes.append("LIQUIDITY_EXPANSION")
    if vr is not None and vr < 0.8: regimes.append("LIQUIDITY_CONTRACTION")
    if vol is not None and vol > 3: regimes.append("HIGH_VOLATILITY")
    if vol is not None and vol < 1: regimes.append("LOW_VOLATILITY")
    primary = regimes[0] if regimes else ("RANGE_BOUND" if r20 is not None else "UNKNOWN_MARKET_REGIME")
    return {"regime":primary,"all_regimes":regimes,"regime_data_status":"READY","index_features":index_features,"uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}

def build_market_regime(*, sample: dict, index_data: dict) -> dict:
    idx_bars = index_data.get("bars",{}) if index_data else {}
    features = _build_index_features(idx_bars, sample.get("entry_date",""))
    return classify_market_regime(index_features=features)
