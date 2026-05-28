from __future__ import annotations
from zmatrix.regime_conditioned_replay.schema import DEFAULT_REGIME_REPLAY_HURDLES

def judge_replay_candidate(*, result: dict, hurdles: dict | None = None) -> dict:
    h = dict(DEFAULT_REGIME_REPLAY_HURDLES)
    if hurdles: h.update(hurdles)
    m = result.get("metrics",{})
    d = result.get("delta_vs_raw",{})
    reasons = []
    if h.get("must_improve_vs_mechanical_stop") and result.get("mechanical_stop_comparison",{}).get("improved") is False:
        reasons.append("NOT_IMPROVED_VS_MECHANICAL_STOP")
    if result.get("kept_count",0) < h["min_kept_count"]: reasons.append("LOW_SAMPLE_COUNT")
    if result.get("kept_rate") is not None and result["kept_rate"] < h["min_kept_rate"]: reasons.append("KEPT_RATE_TOO_LOW")
    if d.get("win_rate_delta") is not None and d["win_rate_delta"] < h["min_win_rate_delta_vs_raw"]: reasons.append("WIN_RATE_DELTA_TOO_SMALL")
    if d.get("median_delta") is not None and d["median_delta"] < h["min_median_delta_vs_raw"]: reasons.append("MEDIAN_DELTA_TOO_SMALL")
    if d.get("trimmed_mean_delta") is not None and d["trimmed_mean_delta"] < h["min_trimmed_mean_delta_vs_raw"]: reasons.append("TRIMMED_MEAN_DELTA_TOO_SMALL")
    if m.get("top_1pct_contribution") is not None and m["top_1pct_contribution"] > h["max_top_1pct_contribution"]: reasons.append("STILL_OUTLIER_DOMINATED")
    if result.get("opportunity_loss_rate") is not None and result["opportunity_loss_rate"] > h["max_opportunity_loss_rate"]: reasons.append("OPPORTUNITY_LOSS_TOO_HIGH")
    status = "POLICY_READY_FOR_OBSERVATION" if not reasons else "POLICY_REJECTED_NO_IMPROVEMENT"
    return {"status":status,"reasons":reasons,"production_ready":False,"real_trade_allowed":False,"broker_order_allowed":False}

def judge_all_replay_candidates(*, replay: dict) -> dict:
    verdicts = {}
    for name, r in replay.get("policy_results",{}).items(): verdicts[name] = judge_replay_candidate(result=r)
    ready = [n for n,v in verdicts.items() if v.get("status")=="POLICY_READY_FOR_OBSERVATION"]
    return {"verdict_report_version":"V357_CANDIDATE_VERDICT_V10","ready_policies":ready,"verdicts":verdicts,"real_trade_allowed":False,"broker_order_allowed":False}
