# allowlist: forbidden-token-definition
"""Tests for workspace_guard — agent workspace isolation and forbidden path checks"""
from __future__ import annotations

import os

from zmatrix.agent.workspace_guard import (
    get_agent_workspace_path,
    is_write_allowed,
    validate_write_target,
)


def test_get_workspace_path_contains_agent_id():
    path = get_agent_workspace_path("agent-42")
    assert "agent_workspace" in path
    assert "agent-42" in path


def test_workspace_write_allowed():
    cwd = os.getcwd()
    ws = get_agent_workspace_path("agent-7")
    target = os.path.join(ws, "research_notes", "output.json")
    assert is_write_allowed("agent-7", target) is True


def test_workspace_escape_rejected():
    ws = get_agent_workspace_path("agent-7")
    target = os.path.join(ws, "..", "..", "zmatrix", "agent", "secret.py")
    assert is_write_allowed("agent-7", target) is False


def test_validate_write_target_forbidden():
    cwd = os.getcwd()
    result = validate_write_target("agent-7", os.path.join(cwd, "zmatrix", "agent", "test.py"))
    assert result["allowed"] is False
    assert "outside" in result["reason"] or "forbidden" in result["reason"]
