"""Script Index v1.0 — 验证与调度脚本索引 (v2.9.10-dev)"""
from __future__ import annotations

SCRIPT_INDEX_REGISTRY = {
    "verify_architecture_candidate": {
        "path":"scripts/verify_architecture_candidate.sh","script_type":"verification",
        "status":"ACTIVE","safe_to_run":True,"writes_data":False,"real_trade_allowed":False,
    },
    "verify_investment_role_candidate": {
        "path":"scripts/verify_investment_role_candidate.sh","script_type":"verification",
        "status":"ACTIVE","safe_to_run":True,"writes_data":False,"real_trade_allowed":False,
    },
    "verify_personal_quant_data_candidate": {
        "path":"scripts/verify_personal_quant_data_candidate.sh","script_type":"verification",
        "status":"ACTIVE","safe_to_run":True,"writes_data":False,"real_trade_allowed":False,
    },
}

def list_script_index() -> dict:
    return dict(SCRIPT_INDEX_REGISTRY)

def check_script_index_integrity() -> list[str]:
    violations = []
    for sid, s in SCRIPT_INDEX_REGISTRY.items():
        if s.get("real_trade_allowed"): violations.append(f"{sid}: real_trade_allowed should be False")
    return violations
