"""Phase 3-A.1: Market Data Privacy Guardrail (hardened)."""
from __future__ import annotations
import subprocess
from pathlib import Path

FORBIDDEN_PATTERNS = [
    ".xlsx", ".xls", ".vendor.csv", ".raw.csv",
    "wind", "choice", "tushare", "akshare",
    "行情", "日线", "分钟", "指数",
]

ALLOWED_PREFIXES = [
    "tests/fixtures/market_data/",
    "templates/research_db/market_data/",
]


def scan_tracked_market_data_files() -> dict:
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    violations = []
    for line in r.stdout.splitlines():
        lower = line.lower()
        if not lower.startswith("data/research_db/market_data/"):
            continue
        if lower.endswith(".gitkeep"):
            continue
        if any(lower.startswith(p) for p in ALLOWED_PREFIXES):
            continue
        for pat in FORBIDDEN_PATTERNS:
            if pat.lower() in lower:
                violations.append(line)
                break
        if "raw/" in lower or "staging/" in lower or "vendor/" in lower:
            violations.append(line)
    return {"status": "PASS" if not violations else "FAILED", "violations": violations, "production_allowed": False}


def assert_no_private_market_data_tracked() -> None:
    result = scan_tracked_market_data_files()
    if result["violations"]:
        raise AssertionError(f"private/vendor market data tracked: {result['violations']}")


def assert_market_fixture_only(tracked_paths: list[str]) -> None:
    for p in tracked_paths:
        if not p.startswith("tests/fixtures/market_data/") and not p.startswith("templates/research_db/market_data/"):
            if p.endswith(".gitkeep") or p.endswith("README.md"):
                continue
            if "data/research_db/market_data/" in p:
                raise AssertionError(f"non-fixture market data tracked: {p}")
