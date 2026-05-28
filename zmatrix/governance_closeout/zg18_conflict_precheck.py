from __future__ import annotations
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY

def precheck_zg18_conflict_risk(*, policies: list[str], market_regime_status: str | None = None) -> dict:
    conflicts = []
    if "allow_b_rotation_in_bull_trend_only" in policies: conflicts.append({"policy":"allow_b_rotation_in_bull_trend_only","risk":"Trend family may dominate; oscillation family suppressed."})
    if "range_bound_observation_only" in policies: conflicts.append({"policy":"range_bound_observation_only","risk":"Range-bound downgrade may conflict with oscillation strategies."})
    if "block_b_rotation_in_bear_trend" in policies: conflicts.append({"policy":"block_b_rotation_in_bear_trend","risk":"Bear trend block may conflict with capitulation/rebound catchers."})
    return {"precheck_version":"V357_ZG18_CONFLICT_PRECHECK_V10","conflict_precheck_status":"CONFLICT_RISK_WARNING" if conflicts else "NO_CONFLICT_RISK_DETECTED","market_regime_status":market_regime_status,"potential_conflicts":conflicts,"state_lock_required":bool(conflicts),"l25_macro_state_lock_required":bool(conflicts),"g18_conflict_resolver_write_allowed":False,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
