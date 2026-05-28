from __future__ import annotations
from zmatrix.research_os_rc.schema import DEFAULT_RESEARCH_OS_RC_SAFETY

def build_rc_verdict(*, evidence_chain: dict, safety_gate: dict, namespace_freeze: dict, data_foundation: dict, replay_readiness: dict) -> dict:
    blockers=[]; warnings=[]
    if evidence_chain.get("evidence_chain_status")!="READY": blockers.append("MISSING_EVIDENCE_CHAIN")
    if safety_gate.get("safety_gate_status")!="PASS": blockers.append("SAFETY_GATE_FAIL")
    if namespace_freeze.get("namespace_status")!="PASS": blockers.append("NAMESPACE_FREEZE_FAIL")
    if data_foundation.get("data_foundation_status")!="READY": blockers.append("DATA_FOUNDATION_INSUFFICIENT")
    if replay_readiness.get("replay_readiness_status")!="READY": warnings.append("REPLAY_READINESS_PARTIAL")
    if namespace_freeze.get("legacy_locked_warning"): warnings.append("LEGACY_LOCKED_WARNING")
    status="RESEARCH_OS_RC_BLOCKED_MISSING_EVIDENCE"
    if not blockers:
        status="RESEARCH_OS_RC_READY_WITH_LOCKED_WARNINGS" if warnings else "RESEARCH_OS_RC_READY"
    return {"verdict_version":"V3520_RC_VERDICT_V10","rc_status":status,"blockers":blockers,"warnings":warnings,"legacy_locked_warning":"LEGACY_LOCKED_WARNING" in warnings,"research_ready":status in ("RESEARCH_OS_RC_READY","RESEARCH_OS_RC_READY_WITH_LOCKED_WARNINGS"),"production_ready":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"safety":dict(DEFAULT_RESEARCH_OS_RC_SAFETY)}
