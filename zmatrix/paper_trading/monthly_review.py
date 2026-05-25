"""Monthly Review Report v1.0"""
from __future__ import annotations
from datetime import datetime

def build_monthly_review(paper_entries: list[dict], outcomes: list[dict], portfolio_snapshot: list[dict] | None = None) -> dict:
    now = datetime.now()
    role_breakdown = {}
    for e in paper_entries:
        r = e.get("role", "UNKNOWN")
        role_breakdown.setdefault(r, 0)
        role_breakdown[r] += 1

    win_count = 0
    returns_t20 = []
    for o in outcomes:
        r = o.get("actual_return_t20")
        if r is not None:
            returns_t20.append(r)
            if r > 0: win_count += 1

    discipline_violations = []
    for e in paper_entries:
        if e.get("role") == "D_REJECT":
            discipline_violations.append({"paper_id": e.get("paper_id"), "reason": "D_REJECT paper entry"})

    return {
        "month": now.strftime("%Y-%m"),
        "paper_count": len(paper_entries),
        "win_rate": round(win_count / len(outcomes) * 100, 1) if outcomes else 0.0,
        "avg_return_t20": round(sum(returns_t20) / len(returns_t20), 2) if returns_t20 else None,
        "discipline_violation_count": len(discipline_violations),
        "top_error_types": [],
        "role_breakdown": role_breakdown,
        "sector_breakdown": {},
        "chain_breakdown": {},
        "review_actions": [],
        "real_trade_allowed": False,
    }
