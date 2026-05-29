# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_HURDLES

def judge_entry_candidate(*, candidate: dict, hurdles: dict | None = None) -> dict:
    h = dict(DEFAULT_ENTRY_REPAIR_HURDLES)
    if hurdles: h.update(hurdles)
    rule = candidate.get("rule",{}); metrics = candidate.get("metrics",{}); delta = candidate.get("delta",{})
    reasons = []
    if rule.get("lookahead_risk") is True: reasons.append("LOOKAHEAD_RISK")
    if candidate.get("kept_count",0) < h["min_kept_count"]: reasons.append("LOW_SAMPLE_COUNT")
    if candidate.get("kept_rate") is not None and candidate.get("kept_rate") < h["min_kept_rate"]: reasons.append("KEPT_RATE_TOO_LOW")
    if delta.get("win_rate_delta") is not None and delta["win_rate_delta"] < h["min_win_rate_delta"]: reasons.append("WIN_RATE_DELTA_TOO_SMALL")
    if delta.get("median_delta") is not None and delta["median_delta"] < h["min_median_delta"]: reasons.append("MEDIAN_DELTA_TOO_SMALL")
    if delta.get("trimmed_mean_delta") is not None and delta["trimmed_mean_delta"] < h["min_trimmed_mean_delta"]: reasons.append("TRIMMED_MEAN_DELTA_TOO_SMALL")
    if metrics.get("top_1pct_contribution") is not None and metrics["top_1pct_contribution"] > h["max_top_1pct_contribution"]: reasons.append("STILL_OUTLIER_DOMINATED")
    status = "CANDIDATE_READY_FOR_PAPER_REPLAY" if not reasons else "CANDIDATE_REJECTED_NO_IMPROVEMENT"
    return {"verdict_version":"V355_ENTRY_CANDIDATE_VERDICT_V10","status":status,"reasons":reasons,"production_ready":False,"real_trade_allowed":False,"broker_order_allowed":False}

def judge_all_entry_candidates(*, replay: dict) -> dict:
    verdicts = {}
    for name, candidate in replay.get("candidates",{}).items(): verdicts[name] = judge_entry_candidate(candidate=candidate)
    ready = [name for name, v in verdicts.items() if v.get("status")=="CANDIDATE_READY_FOR_PAPER_REPLAY"]
    return {"verdict_report_version":"V355_ENTRY_CANDIDATE_VERDICT_REPORT_V10","ready_candidates":ready,"verdicts":verdicts,"real_trade_allowed":False,"broker_order_allowed":False}
