# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_conditioned_replay.regime_policy_library import REGIME_POLICIES, apply_regime_policy
from zmatrix.regime_conditioned_replay.replay_metrics import build_replay_metrics
from zmatrix.regime_conditioned_replay.schema import DEFAULT_REGIME_REPLAY_SAFETY

def run_regime_policy_replay(*, rows: list[dict]) -> dict:
    base_raw = build_replay_metrics(rows=rows)
    results = {}
    for name in REGIME_POLICIES:
        applied = apply_regime_policy(rows=rows, policy_name=name)
        m = build_replay_metrics(rows=applied["kept"])
        opp_returns = [r.get("actual_return_t20") for r in applied.get("downgraded",[]) if r.get("actual_return_t20","") is not None]
        opp_returns = [x for x in opp_returns if isinstance(x,(int,float))]
        opp_wins = [x for x in opp_returns if x>0]
        opp_rate = len(opp_wins)/len(opp_returns) if opp_returns else None
        opp_total = sum(opp_returns) if opp_returns else None
        results[name] = {"policy":applied["policy"],"original_count":applied["original_count"],"kept_count":applied["kept_count"],"downgraded_count":applied["downgraded_count"],"kept_rate":applied["kept_rate"],"metrics":m,"opportunity_loss_rate":opp_rate,"opportunity_loss_total":opp_total,"delta_vs_raw":_delta(base_raw,m)}
    return {"replay_version":"V357_REGIME_POLICY_REPLAY_V10","baseline_raw":base_raw,"policy_results":results,"safety":dict(DEFAULT_REGIME_REPLAY_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}

def _delta(b,n):
    def d(k): return n[k]-b[k] if b.get(k) is not None and n.get(k) is not None else None
    return {"win_rate_delta":d("win_rate"),"median_delta":d("median"),"mean_delta":d("mean"),"trimmed_mean_delta":d("trimmed_mean_5pct"),"invalidation_rate_delta":d("invalidation_rate"),"top_1pct_contribution_delta":d("top_1pct_contribution")}
