# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def observe_zg18_conflicts(*, full_sample_pass_policies: list[str]) -> dict:
    conflicts = []
    for p in full_sample_pass_policies or []:
        if p=="allow_b_rotation_in_bull_trend_only": conflicts.append({"policy":p,"family":"trend_vs_oscillation","risk":"Bull-only gating may suppress oscillation strategies during range-to-trend transition."})
        elif p=="range_bound_observation_only": conflicts.append({"policy":p,"family":"range_policy_vs_oscillation","risk":"Range-bound observation may conflict with oscillation-family candidates."})
        elif p=="block_b_rotation_in_bear_trend": conflicts.append({"policy":p,"family":"bear_block_vs_capitulation_catcher","risk":"Bear block may conflict with left-tail rebound catcher."})
    return {"observer_version":"V358_ZG18_CONFLICT_OBSERVER_V10","conflict_observation_status":"CONFLICT_RISK_WARNING" if conflicts else "NO_CONFLICT_RISK_DETECTED","potential_conflict_count":len(conflicts),"conflict_families":conflicts,"state_lock_required":bool(conflicts),"l25_macro_state_lock_required":bool(conflicts),"g18_conflict_resolver_write_allowed":False,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
