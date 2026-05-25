"""Monthly Review Report v1.0"""
from __future__ import annotations
from datetime import datetime

def build_monthly_review(paper_entries, outcomes, portfolio_snapshot=None):
    now=datetime.now()
    role_breakdown={}
    for e in paper_entries:
        r=e.get("role","UNKNOWN"); role_breakdown[r]=role_breakdown.get(r,0)+1
    returns_t20=[o.get("actual_return_t20") for o in outcomes if o.get("actual_return_t20") is not None]
    valid_count=len(returns_t20)
    win_count=sum(1 for r in returns_t20 if r>0)
    violations=[]
    for e in paper_entries:
        if e.get("role")=="D_REJECT": violations.append({"paper_id":e.get("paper_id"),"reason":"D_REJECT paper entry"})
    insufficient_count=sum(1 for o in outcomes if o.get("actual_return_t20") is None)
    return {
        "month":now.strftime("%Y-%m"),"paper_count":len(paper_entries),
        "win_rate":round(win_count/valid_count*100,1) if valid_count else 0.0,
        "valid_outcome_count":valid_count,"insufficient_outcome_count":insufficient_count,
        "avg_return_t20":round(sum(returns_t20)/valid_count,2) if valid_count else None,
        "discipline_violation_count":len(violations),
        "role_breakdown":role_breakdown,"sector_breakdown":{},"chain_breakdown":{},
        "review_actions":[],"real_trade_allowed":False,
    }
