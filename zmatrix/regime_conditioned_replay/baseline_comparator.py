# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_conditioned_replay.schema import DEFAULT_REGIME_REPLAY_SAFETY

def compare_vs_raw(*, policy_result: dict, baseline_raw: dict) -> dict:
    m = policy_result.get("metrics",{})
    def d(k): return m.get(k)-baseline_raw.get(k) if m.get(k) is not None and baseline_raw.get(k) is not None else None
    return {"win_rate_delta":d("win_rate"),"median_delta":d("median"),"mean_delta":d("mean"),"trimmed_mean_delta":d("trimmed_mean_5pct"),"invalidation_delta":d("invalidation_rate"),"top1pct_delta":d("top_1pct_contribution"),"real_trade_allowed":False,"broker_order_allowed":False}

def compare_all_policies(*, replay: dict) -> dict:
    b = replay.get("baseline_raw",{})
    comps = {}
    for name, r in replay.get("policy_results",{}).items(): comps[name] = compare_vs_raw(policy_result=r, baseline_raw=b)
    return {"comparison_version":"V357_BASELINE_COMPARISON_V10","baseline_raw":b,"policy_comparisons":comps,"mechanical_stop_baseline_status":"MISSING","safety":dict(DEFAULT_REGIME_REPLAY_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
