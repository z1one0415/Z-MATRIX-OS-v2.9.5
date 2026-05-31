# allowlist: forbidden-token-definition
"""Tests for agent_registry — load, get, validate, assert"""
from __future__ import annotations

import json
import os
import tempfile

import pytest

from zmatrix.agent.agent_registry import (
    assert_agent_enabled,
    assert_agent_scope,
    get_agent,
    load_agent_registry,
    validate_agent_entry,
)


VALID_ENTRY = {
    "agent_id": "test-agent",
    "agent_name": "Test Agent",
    "agent_type": "RESEARCH",
    "permission_level": "VIEW_ONLY",
    "allowed_scopes": ["research_summary"],
    "allowed_read_layers": ["docs"],
    "allowed_write_layers": [],
    "allowed_commands": ["QUERY"],
    "forbidden_commands": ["REAL_TRADE"],
    "max_risk_level": "R2_DRAFT",
    "requires_human_review": True,
    "workspace_path": "runtime/workspace/test-agent",
    "enabled": True,
    "production_allowed": False,
    "owner": "system",
    "role": "Tester",
    "created_at": "2026-05-31T00:00:00Z",
}


def _write_registry(entries: list[dict]) -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh)
    return path


class TestLoadAgentRegistry:
    def test_load_valid_registry_returns_list(self):
        entries = [dict(VALID_ENTRY)]
        path = _write_registry(entries)
        try:
            result = load_agent_registry(path)
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["agent_id"] == "test-agent"
        finally:
            os.unlink(path)

    def test_get_agent_for_known_agent(self):
        entries = [dict(VALID_ENTRY)]
        path = _write_registry(entries)
        try:
            agent = get_agent("test-agent", path)
            assert isinstance(agent, dict)
            assert agent["agent_id"] == "test-agent"
            assert agent["agent_name"] == "Test Agent"
        finally:
            os.unlink(path)

    def test_get_agent_for_unknown_agent_raises(self):
        entries = [dict(VALID_ENTRY)]
        path = _write_registry(entries)
        try:
            with pytest.raises(KeyError, match="Unknown agent"):
                get_agent("nonexistent", path)
        finally:
            os.unlink(path)

    def test_load_with_missing_file_returns_empty_list(self):
        result = load_agent_registry("/nonexistent/path/registry.json")
        assert result == []


class TestValidateAgentEntry:
    def test_valid_entry_passes(self):
        result = validate_agent_entry(VALID_ENTRY)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_production_allowed_true_is_error(self):
        entry = dict(VALID_ENTRY, production_allowed=True)
        result = validate_agent_entry(entry)
        assert result["valid"] is False
        assert any("production_allowed" in e for e in result["errors"])

    def test_allowed_scopes_wildcard_is_error(self):
        entry = dict(VALID_ENTRY, allowed_scopes=["*"])
        result = validate_agent_entry(entry)
        assert result["valid"] is False
        assert any("wildcard" in e for e in result["errors"])

    def test_requires_human_review_false_with_r3_is_error(self):
        entry = dict(
            VALID_ENTRY,
            requires_human_review=False,
            max_risk_level="R3_WRITE_RESEARCH_DB",
        )
        result = validate_agent_entry(entry)
        assert result["valid"] is False
        assert any("requires_human_review" in e for e in result["errors"])


class TestAssertAgentEnabled:
    def test_enabled_agent_returns_success(self):
        entries = [dict(VALID_ENTRY, enabled=True)]
        path = _write_registry(entries)
        try:
            result = assert_agent_enabled("test-agent", path)
            assert result["allowed"] is True
            assert result["reason"] == ""
        finally:
            os.unlink(path)

    def test_disabled_agent_returns_rejection(self):
        entries = [dict(VALID_ENTRY, enabled=False)]
        path = _write_registry(entries)
        try:
            result = assert_agent_enabled("test-agent", path)
            assert result["allowed"] is False
            assert "disabled" in result["reason"].lower()
        finally:
            os.unlink(path)
