"""BRD Historical Replay v3.2 — PIT Feature Builder (point-in-time, no future leak)"""
from __future__ import annotations
import csv
from statistics import mean
from pathlib import Path

DEFAULT_PIT_FEATURE_SAFETY = {
    "future_data_allowed": False, "real_trade_allowed": False,
    "broker_order_allowed": False, "auto_buy_allowed": False,
    "auto_sell_allowed": False, "auto_position_close_allowed": False,
    "real_z9_write_allowed": False, "hermes_memory_write_allowed": False,
    "auto_calibration_allowed": False, "prompt_auto_injection_allowed": False,
    "system_prompt_write_allowed": False, "runtime_enabled": False,
}


def _clean_date(x: str) -> str: return str(x or "").replace("-", "").strip()
def _to_float(x, default=0.0):
    try: return float(x) if x not in (None, "") else default
    except: return default

def _pct_change(cur, prev): return (cur / prev - 1.0) if prev and prev > 0 else None
def _rolling_return(closes, n):
    return _pct_change(closes[-1], closes[-1 - n]) if len(closes) > n else None

def _rolling_ma(closes, n): return mean(closes[-n:]) if len(closes) >= n else None

def _rolling_volatility(closes, n) -> float | None:
    if len(closes) < n + 1: return None
    rets = [_pct_change(closes[i], closes[i-1]) for i in range(1,len(closes)) if closes[i-1]>0]
    rets = [r for r in rets if r is not None]
    return (sum((r-mean(rets))**2 for r in rets)/(len(rets)-1))**0.5 if len(rets) >= 2 else None


def _load_bars_until(*, ticker, replay_date, local_data_root):
    bare = ticker.split(".")[0]  # strip .SZ/.SH/.BJ suffix
    path = Path(local_data_root) / "data" / "price_bars" / f"{bare}.csv"
    if not path.exists(): return []
    clean_r = _clean_date(replay_date)
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = _clean_date(r.get("trade_date") or r.get("date")); d = d.zfill(8) if d and len(d) < 8 else d
            if not d: continue
            if d <= clean_r:
                rows.append({"trade_date": d, "open": _to_float(r.get("open")),
                             "high": _to_float(r.get("high")), "low": _to_float(r.get("low")),
                             "close": _to_float(r.get("close")),
                             "volume": _to_float(r.get("vol") or r.get("volume")),
                             "amount": _to_float(r.get("amount"))})
            else: break
    return rows


def build_pit_features(*, ticker, replay_date, local_data_root, min_history_days=120):
    bars = _load_bars_until(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root)
    if len(bars) < min_history_days:
        return {"feature_version": "PIT_FEATURES_V10", "ticker": ticker,
                "replay_date": replay_date, "feature_status": "INSUFFICIENT_HISTORY",
                "history_days": len(bars), "features": {},
                "future_data_allowed": False, "safety": dict(DEFAULT_PIT_FEATURE_SAFETY)}
    closes = [b["close"] for b in bars if b.get("close", 0) > 0]
    volumes = [b["volume"] for b in bars if b.get("volume", 0) >= 0]
    latest = bars[-1]
    close = latest["close"]
    ma20, ma60, ma120 = _rolling_ma(closes, 20), _rolling_ma(closes, 60), _rolling_ma(closes, 120)
    features = {
        "close": close, "return_5d": _rolling_return(closes, 5),
        "return_20d": _rolling_return(closes, 20), "return_60d": _rolling_return(closes, 60),
        "return_120d": _rolling_return(closes, 120),
        "ma20": ma20, "ma60": ma60, "ma120": ma120,
        "above_ma20": close > ma20 if ma20 else None,
        "above_ma60": close > ma60 if ma60 else None,
        "above_ma120": close > ma120 if ma120 else None,
        "volatility_20d": _rolling_volatility(closes, 20),
        "volatility_60d": _rolling_volatility(closes, 60),
        "volume_ratio_20d": volumes[-1]/mean(volumes[-20:]) if len(volumes)>=20 and mean(volumes[-20:])>0 else None,
        "history_days": len(bars),
    }
    return {"feature_version": "PIT_FEATURES_V10", "ticker": ticker,
            "replay_date": replay_date, "feature_status": "READY",
            "history_days": len(bars), "features": features,
            "last_bar_date": latest["trade_date"],
            "price_snapshot": {"close": close, "open": latest["open"], "high": latest["high"],
                              "low": latest["low"], "volume": latest["volume"]},
            "future_data_allowed": False, "real_trade_allowed": False, "broker_order_allowed": False,
            "safety": dict(DEFAULT_PIT_FEATURE_SAFETY)}
