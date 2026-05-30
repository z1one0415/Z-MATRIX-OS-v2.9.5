"""Phase 3-A: Market Data Privacy Guardrail."""
from __future__ import annotations

FORBIDDEN_FILE_PATTERNS = [
    ".xlsx", ".xls", ".vendor.csv", ".raw.csv",
    "wind", "choice", "tushare", "akshare",
    "行情", "日线", "分钟", "指数",
]

def check_market_data_tracking(tracked_paths: list[str]) -> dict:
    violations = []
    for p in tracked_paths:
        lower = p.lower()
        if "data/research_db/market_data/raw/" in lower and not p.endswith(".gitkeep"):
            violations.append(p)
        if "data/research_db/market_data/staging/" in lower and not p.endswith(".gitkeep"):
            violations.append(p)
        if "data/research_db/market_data/vendor/" in lower and not p.endswith(".gitkeep"):
            violations.append(p)
        for pat in FORBIDDEN_FILE_PATTERNS:
            if pat.lower() in lower:
                violations.append(p); break
    return {"status": "PASS" if not violations else "FAILED", "violations": violations, "production_allowed": False}
