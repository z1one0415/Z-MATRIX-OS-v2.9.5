# allowlist: forbidden-token-definition
"""Agent Tamper Guard — scans files for forbidden flags, dangerous calls, and secrets"""
from __future__ import annotations

import os
import re

FORBIDDEN_FLAGS = [
    r'real_trade_allowed\s*=\s*True',
    r'broker_order_allowed\s*=\s*True',
    r'runtime_enabled\s*=\s*True',
    r'auto_buy_allowed\s*=\s*True',
    r'auto_sell_allowed\s*=\s*True',
    r'production_allowed\s*=\s*True',
    r'production_strategy_modified\s*=\s*True',
    r'allowed_scopes\s*=\s*\[\s*["\']\*["\']\s*\]',
    r'allowed_scopes\s*=\s*\[["\']\*["\']\]',
    r'requires_human_review\s*=\s*false',
    r'requires_human_review\s*=\s*False',
]

DANGEROUS_CALLS = [
    r'\bsubprocess\b',
    r'\bos\.system\s*\(',
    r'\beval\s*\(',
    r'\bexec\s*\(',
    r'\bcurl\b',
    r'\brequests\.post\s*\(',
    r'\bhttpx\.post\s*\(',
]

SECRET_PATTERNS = [
    r'api_key\s*=\s*["\'][^"\']+["\']',
    r'token\s*=\s*["\'][^"\']{8,}["\']',
    r'secret\s*=\s*["\'][^"\']+["\']',
]


def scan_for_forbidden_flags(content: str) -> list[str]:
    findings: list[str] = []
    for pattern in FORBIDDEN_FLAGS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append(pattern)
    return findings


def scan_for_dangerous_calls(content: str) -> list[str]:
    findings: list[str] = []
    for pattern in DANGEROUS_CALLS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append(pattern)
    return findings


def scan_for_secrets(content: str) -> list[str]:
    findings: list[str] = []
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append(pattern)
    return findings


def run_tamper_check(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {"passed": True, "findings": []}
    with open(file_path, "r", encoding="utf-8") as fh:
        content = fh.read()
    all_findings: list[str] = []
    all_findings.extend(scan_for_forbidden_flags(content))
    all_findings.extend(scan_for_dangerous_calls(content))
    all_findings.extend(scan_for_secrets(content))
    return {"passed": len(all_findings) == 0, "findings": all_findings}
