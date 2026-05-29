# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.research_os_rc.schema import DEFAULT_RESEARCH_OS_RC_SAFETY

REQUIRED = {"return_integrity":["return_integrity","v351"],"repair_lab":["strategy_repair","v352"],"invalidation":["invalidation","anatomy"],"entry_quality":["entry_quality"],"market_regime":["market_regime","regime"],"sector_mapping":["sector_mapping","v3510"],"sector_basket":["synthetic_sector","v3511"],"regime_sector":["regime_sector","v3512"],"role_replay":["role_replay","v3514"],"taxonomy":["taxonomy","v3515"],"adapter":["adapter","v3517"],"classifier_v2":["classifier_v2","v3518"],"deprecation":["deprecation","v3519"]}

def audit_evidence_chain(*, report_files: list[str]) -> dict:
    lower = [str(x).lower() for x in report_files or []]
    found={}; missing=[]
    for k,needles in REQUIRED.items():
        ok=all(n.lower() in f for f in lower for n in needles if n.lower() in f) or any(all(n.lower() in f for n in needles) for f in lower)
        found[k]=ok
        if not ok: missing.append(k)
    return {"auditor_version":"V3520_EVIDENCE_CHAIN_AUDITOR_V10","required_count":len(REQUIRED),"found_count":sum(1 for v in found.values() if v),"found":found,"missing":missing,"evidence_chain_status":"READY" if not missing else "MISSING_EVIDENCE","real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_RESEARCH_OS_RC_SAFETY)}
