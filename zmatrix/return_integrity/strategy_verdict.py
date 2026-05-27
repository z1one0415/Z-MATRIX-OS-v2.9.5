from __future__ import annotations

def build_strategy_verdict(*, robust_metrics: dict, audit_report: dict | None = None) -> dict:
    win_rate = robust_metrics.get("win_rate")
    median = robust_metrics.get("median")
    trimmed = robust_metrics.get("trimmed_mean_5pct")
    top_contribution = robust_metrics.get("top_1pct_contribution")
    reasons = []
    if robust_metrics.get("valid_return_count", 0) <= 0:
        return _verdict("BLOCKED_INSUFFICIENT_VALID_RETURNS", ["no valid returns"])
    if median is not None and median < 0:
        reasons.append("NEGATIVE_MEDIAN_RETURN")
    if win_rate is not None and win_rate < 0.5:
        reasons.append("WIN_RATE_BELOW_50_PERCENT")
    if trimmed is not None and trimmed < 0:
        reasons.append("NEGATIVE_TRIMMED_MEAN")
    if top_contribution is not None and top_contribution > 0.5:
        reasons.append("TOP_1PCT_DOMINATES_RETURN")
    if reasons:
        if "TOP_1PCT_DOMINATES_RETURN" in reasons:
            return _verdict("BLOCKED_OUTLIER_DOMINATED", reasons)
        if "NEGATIVE_MEDIAN_RETURN" in reasons:
            return _verdict("BLOCKED_NEGATIVE_MEDIAN", reasons)
        if "WIN_RATE_BELOW_50_PERCENT" in reasons:
            return _verdict("BLOCKED_LOW_WIN_RATE", reasons)
        return _verdict("WEAK_RIGHT_TAIL_ONLY", reasons)
    return _verdict("PERFORMANCE_QUALIFIED", [])

def _verdict(status: str, reasons: list[str]) -> dict:
    return {"verdict_version": "STRATEGY_VERDICT_V10", "performance_status": status, "reasons": reasons, "live_trading_permission": False, "real_trade_allowed": False, "broker_order_allowed": False}
