from __future__ import annotations
import math
from statistics import median

def _clean(xs):
    return [float(x) for x in xs if x is not None and not math.isnan(float(x))]

def _mean(xs):
    xs = _clean(xs)
    return sum(xs) / len(xs) if xs else None

def _percentile(xs, p):
    xs = sorted(_clean(xs))
    if not xs:
        return None
    k = int(round((len(xs) - 1) * p))
    return xs[k]

def _trimmed_mean(xs, trim=0.05):
    xs = sorted(_clean(xs))
    if not xs:
        return None
    n = len(xs)
    k = int(n * trim)
    xs2 = xs[k:n-k] if n > 2 * k else xs
    return sum(xs2) / len(xs2) if xs2 else None

def _winsorized_mean(xs, trim=0.05):
    xs = sorted(_clean(xs))
    if not xs:
        return None
    n = len(xs)
    k = int(n * trim)
    lo = xs[k] if k < n else xs[0]
    hi = xs[n - k - 1] if k < n else xs[-1]
    ys = [min(max(x, lo), hi) for x in xs]
    return sum(ys) / len(ys)

def build_robust_return_metrics(*, outcomes: list[dict], horizon: str = "t20") -> dict:
    key = f"actual_return_{horizon.lower()}"
    returns = [o.get(key) for o in outcomes if o.get("outcome_status") == "READY" and o.get(key) is not None]
    xs = _clean(returns)
    wins = [x for x in xs if x > 0]
    top_1pct_cut = _percentile(xs, 0.99)
    top_contribution = None
    if xs and top_1pct_cut is not None:
        top = [x for x in xs if x >= top_1pct_cut]
        total_sum = sum(xs)
        top_contribution = sum(top) / total_sum if total_sum else None
    return {"metrics_version": "ROBUST_RETURN_METRICS_V10", "horizon": horizon.upper(), "sample_count": len(outcomes), "valid_return_count": len(xs), "win_rate": len(wins) / len(xs) if xs else None, "mean": _mean(xs), "median": median(xs) if xs else None, "trimmed_mean_5pct": _trimmed_mean(xs, 0.05), "winsorized_mean_5pct": _winsorized_mean(xs, 0.05), "p05": _percentile(xs, 0.05), "p25": _percentile(xs, 0.25), "p75": _percentile(xs, 0.75), "p95": _percentile(xs, 0.95), "p99": _percentile(xs, 0.99), "best": max(xs) if xs else None, "worst": min(xs) if xs else None, "top_1pct_contribution": top_contribution, "real_trade_allowed": False, "broker_order_allowed": False}
