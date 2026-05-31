# allowlist: forbidden-token-definition
"""Tests for mutation prevention — workspace guard, tamper guard, and secret blocker"""
from __future__ import annotations

import os

from zmatrix.agent.tamper_guard import scan_for_forbidden_flags
from zmatrix.agent.workspace_guard import validate_write_target
from zmatrix.agent.security.secret_pattern_blocker import block_if_contains_secrets


def test_workspace_guard_prevents_direct_zmatrix_write():
    cwd = os.getcwd()
    result = validate_write_target("agent-9", os.path.join(cwd, "zmatrix", "foo.py"))
    assert result["allowed"] is False


def test_tamper_guard_blocks_production_flag():
    content = "production_allowed = True"
    findings = scan_for_forbidden_flags(content)
    assert len(findings) > 0
    assert any("production_allowed" in f for f in findings)


def test_secret_blocker_prevents_key_leak():
    result = block_if_contains_secrets('api_key="sk-abc1234567890secretkey"')
    assert result["blocked"] is True
    assert len(result["matches"]) > 0
