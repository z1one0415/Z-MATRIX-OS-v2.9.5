from __future__ import annotations
from zmatrix.strategy_repair.schema import DEFAULT_REPAIR_HURDLES

def judge_repair_candidate(*, candidate: dict, hurdles: dict | None = None) -> dict:
    h = dict(DEFAULT_REPAIR_HURDLES)
    if hurdles: h.update(hurdles)
    rule = candidate.get("rule", {})
    metrics = candidate.get("metrics", {})
    delta = candidate.get("delta", {})
    reasons = []
    if candidate.get("kept_count", 0) < h["min_active_count"]: reasons.append("INSUFFICIENT_KEPT_SAMPLE")
    if rule.get("lookahead_risk"): reasons.append("LOOKAHEAD_RISK")
    if delta.get("win_rate_delta") is not None and delta.get("win_rate_delta") < h["min_win_rate_delta"]: reasons.append("WIN_RATE_DELTA_TOO_SMALL")
    if delta.get("median_delta") is not None and delta.get("median_delta") < h["min_median_delta"]: reasons.append("MEDIAN_DELTA_TOO_SMALL")
    if metrics.get("top_1pct_contribution") is not None and metrics.get("top_1pct_contribution") > h["max_top_1pct_contribution"]: reasons.append("STILL_OUTLIER_DOMINATED")
    status = "REPAIR_CANDIDATE_REJECTED" if reasons else "REPAIR_CANDIDATE_READY"
    return {"repair_verdict_version": "V352_REPAIR_VERDICT_V10", "status": status, "reasons": reasons, "real_trade_allowed": False, "broker_order_allowed": False}

def judge_all_repair_candidates(*, simulation: dict) -> dict:
    verdicts = {}
    for name, candidate in simulation.get("candidates", {}).items():
        verdicts[name] = judge_repair_candidate(candidate=candidate)
    ready = [name for name, v in verdicts.items() if v.get("status") == "REPAIR_CANDIDATE_READY"]
    return {"repair_verdict_report_version": "V352_REPAIR_VERDICT_REPORT_V10", "ready_candidates": ready, "verdicts": verdicts, "real_trade_allowed": False, "broker_order_allowed": False}
