# allowlist: forbidden-token-definition
from __future__ import annotations
from statistics import median
from zmatrix.strategy_repair.schema import DEFAULT_REPAIR_SAFETY

def _clean(xs):
    out = []
    for x in xs:
        if x is None: continue
        try: out.append(float(x))
        except Exception: pass
    return out

def _bucket_return(x):
    if x is None: return "MISSING"
    x = float(x)
    if x <= -20: return "LOSS_20_PLUS"
    if x <= -5: return "LOSS_5_20"
    if x < 0: return "LOSS_0_5"
    if x < 5: return "GAIN_0_5"
    if x < 20: return "GAIN_5_20"
    if x < 120: return "GAIN_20_120"
    return "EXTREME_RIGHT_TAIL"

def build_segment_attribution(*, joined: list[dict], horizon: str = "t20") -> dict:
    key = f"actual_return_{horizon.lower()}"
    dimensions = {
        "role": lambda x: x.get("role", "UNKNOWN"),
        "sector_phase": lambda x: x.get("sector_phase", "UNKNOWN"),
        "invalidation": lambda x: "INVALIDATED" if x.get("invalidation_triggered") else "NOT_INVALIDATED",
        "mae_bucket": lambda x: "HIGH_MAE" if x.get("max_adverse_excursion_pct") is not None and float(x.get("max_adverse_excursion_pct")) < -10 else "NORMAL_MAE",
        "return_bucket": lambda x: _bucket_return(x.get(key)),
    }
    result = {}
    for dim, fn in dimensions.items():
        grouped = {}
        for x in joined or []:
            if x.get("outcome_status") != "READY": continue
            if x.get("paper_action") in ("NO_ACTION", "DATA_GAP", None): continue
            k = fn(x)
            grouped.setdefault(k, []).append(x.get(key))
        result[dim] = {}
        for k, vals in grouped.items():
            xs = _clean(vals)
            wins = [v for v in xs if v > 0]
            result[dim][k] = {"count": len(xs), "win_rate": len(wins) / len(xs) if xs else None, "mean": sum(xs) / len(xs) if xs else None, "median": median(xs) if xs else None}
    return {"segment_report_version": "V352_SEGMENT_ATTRIBUTION_V10", "horizon": horizon.upper(), "segments": result, "safety": dict(DEFAULT_REPAIR_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
