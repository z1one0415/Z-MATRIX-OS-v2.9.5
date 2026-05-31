# allowlist: forbidden-token-definition
"""Secret Pattern Blocker — regex-based secret detection and blocking"""
from __future__ import annotations

import re

SECRET_PATTERNS = [
    re.compile(r'sk-[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    re.compile(r'sk-ant-[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    re.compile(r'AIza[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    re.compile(r'xai-[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    re.compile(r'hf_[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    re.compile(r'ghp_[a-zA-Z0-9]{20,}', re.IGNORECASE),
    re.compile(r'gho_[a-zA-Z0-9]{20,}', re.IGNORECASE),
    re.compile(r'ghu_[a-zA-Z0-9]{20,}', re.IGNORECASE),
    re.compile(r'ghs_[a-zA-Z0-9]{20,}', re.IGNORECASE),
    re.compile(r'ghr_[a-zA-Z0-9]{20,}', re.IGNORECASE),
    re.compile(r'(?:api_key|apikey|api-key)\s*[:=]\s*["\'][^"\']{8,}["\']', re.IGNORECASE),
    re.compile(r'(?:secret|token)\s*[:=]\s*["\'][^"\']{8,}["\']', re.IGNORECASE),
    re.compile(r'(?:OPENAI|ANTHROPIC|GOOGLE|GEMINI|DEEPSEEK)_API_KEY\s*[:=]\s*["\'][^"\']+["\']', re.IGNORECASE),
    re.compile(r'(?:GITHUB|BROKER|EMAIL)_TOKEN\s*[:=]\s*["\'][^"\']+["\']', re.IGNORECASE),
    re.compile(r'Authorization\s*:\s*Bearer\s+[^\s]{8,}', re.IGNORECASE),
    re.compile(r'Bearer\s+[^\s]{8,}', re.IGNORECASE),
]


def scan_text(text: str) -> list[dict]:
    matches: list[dict] = []
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            matches.append({"pattern": pattern.pattern, "match": match.group()})
    return matches


def block_if_contains_secrets(text: str) -> dict:
    matches = scan_text(text)
    if matches:
        return {"blocked": True, "matches": matches}
    return {"blocked": False, "matches": []}
