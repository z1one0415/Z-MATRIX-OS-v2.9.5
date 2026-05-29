# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def build_o3_paper_fallback_study(*, pool_deep_dive: dict) -> dict:
    risky = []
    for name, r in pool_deep_dive.get("policy_pool_deep_results",{}).items():
        if r.get("pool_resilience_deep_status") != "POOL_RESILIENCE_PASS": risky.append({"policy":name,"status":r.get("pool_resilience_deep_status"),"reasons":r.get("reasons",[])})
    return {"study_version":"V358_O3_PAPER_FALLBACK_STUDY_V10","fallback_study_status":"FALLBACK_OBSERVATION_POOL_REQUIRED" if risky else "FALLBACK_NOT_REQUIRED","risky_policies":risky,"paper_observation_pool_plan":{"purpose":"Provide observation-only fallback pool when main pool becomes too narrow.","allowed_actions":["WATCH_ONLY","PAPER_OBSERVATION","NO_ACTION"],"forbidden_actions":["REAL_BUY","REAL_SELL","BROKER_ORDER","AUTO_POSITION_CLOSE"],"runtime_enabled":False},"fallback_pool_generation_allowed":False,"o3_conditional_runtime_enabled":False,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
