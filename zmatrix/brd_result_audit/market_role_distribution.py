# allowlist: forbidden-token-definition
"""Market Role Distribution — full-market BRD role statistics"""
from __future__ import annotations
from collections import Counter,defaultdict
from zmatrix.brd_result_audit.schema import BRD_ROLES, DEFAULT_AUDIT_SAFETY

def build_market_role_distribution_report(*, paper_actions):
    rc=Counter(); ac=Counter(); reasons=Counter(); rr=defaultdict(Counter); total=len(paper_actions or[])
    for a in (paper_actions or[]):
        role=a.get("role") or a.get("source_brd_result",{}).get("role") or "UNKNOWN"
        if role not in BRD_ROLES: role="UNKNOWN"
        rc[role]+=1; ac[a.get("paper_action","UNKNOWN")]+=1
        b=a.get("source_brd_result",{}).get("source_raw",{}).get("b_matrix") or a.get("source_brd_result",{}).get("b_matrix") or {}
        for r in b.get("reason_codes",[]): reasons[r]+=1; rr[role][r]+=1
    rd={r:{"count":rc.get(r,0),"rate":rc.get(r,0)/total if total else None} for r in BRD_ROLES}
    ur=rc.get("UNKNOWN",0)/total if total else None
    active=sum(1 for a in (paper_actions or[]) if a.get("paper_action") not in ("NO_ACTION","DATA_GAP",None))
    st="PASS" if total>=1000 and (ur is None or ur<0.05) else ("WARN_UNKNOWN_RATE_HIGH" if ur and ur>=0.05 else "SMALL_SAMPLE")
    return {"report_version":"BRD_MARKET_ROLE_DISTRIBUTION_V10","total":total,"active_paper_actions":active,
            "active_rate":active/total if total else None,"role_distribution":rd,"paper_action_distribution":dict(ac),
            "top_reason_codes":reasons.most_common(30),"unknown_rate":ur,"distribution_status":st,
            "safety":dict(DEFAULT_AUDIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
