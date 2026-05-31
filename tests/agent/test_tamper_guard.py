# allowlist: forbidden-token-definition
"""Tests for tamper_guard — forbidden flags, dangerous calls, and secret scanning"""
from __future__ import annotations

import os
import tempfile

from zmatrix.agent.tamper_guard import (
    run_tamper_check,
    scan_for_dangerous_calls,
    scan_for_forbidden_flags,
    scan_for_secrets,
)


def test_scan_for_forbidden_flags_detects_production():
    content = 'production_allowed=True'
    findings = scan_for_forbidden_flags(content)
    assert len(findings) >= 1
    assert any('production_allowed' in f for f in findings)


def test_scan_for_forbidden_flags_detects_wildcard():
    content = 'allowed_scopes=["*"]'
    findings = scan_for_forbidden_flags(content)
    assert len(findings) >= 1
    assert any('allowed_scopes' in f for f in findings)


def test_scan_for_dangerous_calls():
    content = 'result = os.system("rm -rf /")'
    findings = scan_for_dangerous_calls(content)
    assert len(findings) >= 1
    assert any('system' in f for f in findings)


def test_scan_for_secrets():
    content = 'api_key="sk-abc123secretkeyhereformatest"'
    findings = scan_for_secrets(content)
    assert len(findings) >= 1
    assert any('api_key' in f for f in findings)


def test_clean_code_passes(tmp_path):
    test_file = tmp_path / "clean.py"
    test_file.write_text("def add(a, b):\n    return a + b\n")
    result = run_tamper_check(str(test_file))
    assert result["passed"] is True
    assert result["findings"] == []
