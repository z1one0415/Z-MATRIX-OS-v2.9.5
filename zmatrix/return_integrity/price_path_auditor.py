from __future__ import annotations
from zmatrix.return_integrity.schema import DEFAULT_RETURN_INTEGRITY_SAFETY

def audit_price_path(*, ticker: str, entry_date: str, price_path: list[float], trade_dates: list[str] | None = None) -> dict:
    issues = []
    if not price_path or len(price_path) < 5:
        issues.append("PRICE_PATH_TOO_SHORT")
    if any(p is None or p <= 0 for p in price_path or []):
        issues.append("NON_POSITIVE_PRICE")
    jumps = []
    for i in range(1, len(price_path or [])):
        prev = price_path[i - 1]
        cur = price_path[i]
        if prev and prev > 0:
            jump = (cur - prev) / prev * 100
            if abs(jump) > 25:
                jumps.append({"idx": i, "prev": prev, "cur": cur, "jump_pct": round(jump, 2)})
    if jumps:
        issues.append("ABNORMAL_SINGLE_DAY_JUMP")
    if trade_dates:
        clean_dates = [str(d).replace("-", "") for d in trade_dates]
        if clean_dates != sorted(clean_dates):
            issues.append("TRADE_DATES_NOT_SORTED")
    return {"audit_version": "PRICE_PATH_AUDIT_V10", "ticker": ticker, "entry_date": entry_date, "path_len": len(price_path or []), "issues": issues, "abnormal_jumps": jumps[:20], "pass": len(issues) == 0, "safety": dict(DEFAULT_RETURN_INTEGRITY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
