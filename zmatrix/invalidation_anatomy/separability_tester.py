# allowlist: forbidden-token-definition
from __future__ import annotations
from statistics import median
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY, DEFAULT_ANATOMY_THRESHOLDS

FEATURE_KEYS = ["time_to_invalidation", "drawdown_speed", "trigger_day_clv", "upper_shadow_pct", "lower_shadow_pct", "intraday_return_pct", "rebound_after_trigger_1d", "rebound_after_trigger_2d"]

def _clean(xs):
    out = []
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except Exception: pass
    return out

def _stat(xs):
    xs = _clean(xs)
    return {"count": len(xs), "mean": sum(xs) / len(xs) if xs else None, "median": median(xs) if xs else None}

def test_path_separability(*, anatomy_rows: list[dict]) -> dict:
    true_bd = [r for r in anatomy_rows if r.get("path_type") in ("TRUE_BREAKDOWN", "STOCK_SPECIFIC_DAMAGE")]
    recovery = [r for r in anatomy_rows if r.get("path_type") in ("FAST_RECOVERY", "SLOW_RECOVERY", "HIGH_VOLATILITY_WINNER", "MARKET_BETA_SHAKEOUT")]
    if len(true_bd) < 100 or len(recovery) < 100: return {"separability_version": "V354_SEPARABILITY_TEST_V10", "separability_status": "DATA_INSUFFICIENT", "true_breakdown_count": len(true_bd), "recovery_count": len(recovery), "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    contrasts = []
    for key in FEATURE_KEYS:
        a_vals = [r.get("features", {}).get(key) for r in true_bd]; b_vals = [r.get("features", {}).get(key) for r in recovery]
        a = _stat(a_vals); b = _stat(b_vals)
        score = abs(a["median"] - b["median"]) / (abs(a["median"]) + abs(b["median"]) + 1e-9) if a["median"] is not None and b["median"] is not None else 0
        contrasts.append({"feature": key, "true_breakdown": a, "recovery": b, "separation_score": score})
    contrasts = sorted(contrasts, key=lambda x: x["separation_score"], reverse=True)
    top = [x["separation_score"] for x in contrasts[:3]]
    sep_score = sum(top) / len(top) if top else 0
    th = DEFAULT_ANATOMY_THRESHOLDS
    status = "SEPARABLE" if sep_score >= th["separable_score"] else "WEAKLY_SEPARABLE" if sep_score >= th["weakly_separable_score"] else "NOT_SEPARABLE"
    return {"separability_version": "V354_SEPARABILITY_TEST_V10", "separability_status": status, "separability_score": sep_score, "true_breakdown_count": len(true_bd), "recovery_count": len(recovery), "top_discriminating_features": contrasts[:10], "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
