from __future__ import annotations
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY

def build_o3_conditional_fallback_plan(*, pool_resilience: dict) -> dict:
    risky = []
    for name, r in pool_resilience.get("policy_pool_results",{}).items():
        if r.get("pool_resilience_status") != "POOL_RESILIENCE_PASS": risky.append({"policy":name,"pool_resilience_status":r.get("pool_resilience_status"),"reasons":r.get("reasons",[])})
    return {"fallback_plan_version":"V357_O3_CONDITIONAL_FALLBACK_PLAN_V10","fallback_plan_status":"FALLBACK_PLAN_REQUIRED" if risky else "FALLBACK_PLAN_NOT_REQUIRED","risky_policies":risky,"paper_only_plan":{"description":"If candidate pool is too small, generate relative defensive observation pool in paper-only mode.","allowed_actions":["WATCH_ONLY","PAPER_OBSERVATION","NO_ACTION"],"forbidden_actions":["REAL_BUY","REAL_SELL","BROKER_ORDER","AUTO_POSITION_CLOSE"]},"o3_conditional_runtime_enabled":False,"fallback_pool_generation_allowed":False,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
