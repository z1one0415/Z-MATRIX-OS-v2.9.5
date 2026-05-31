# allowlist: forbidden-token-definition
"""Tests for skill_registry — load, get, validate, assert"""
from __future__ import annotations

import json
import os
import tempfile

import pytest

from zmatrix.agent.skill_registry import (
    assert_skill_callable,
    get_skill,
    load_skill_registry,
    validate_skill_entry,
)


VALID_SKILL = {
    "skill_id": "TEST.SKILL_READ",
    "skill_name": "Test Skill Read",
    "domain": "SYSTEM_VERIFY",
    "version": "1.0",
    "input_schema_ref": "test_schema",
    "output_schema_ref": "test_output_schema",
    "allowed_callers": ["z-orchestrator"],
    "risk_level": "R0_READ",
    "requires_human_review": False,
    "read_layers": ["test_data"],
    "write_layers": [],
    "verify_script": None,
    "enabled": True,
    "production_allowed": False,
}

VALID_WRITE_SKILL = {
    "skill_id": "TEST.SKILL_WRITE",
    "skill_name": "Test Skill Write",
    "domain": "AUTOCASEFORGE",
    "version": "1.0",
    "input_schema_ref": "test_write_schema",
    "output_schema_ref": "test_write_output_schema",
    "allowed_callers": ["z-orchestrator"],
    "risk_level": "R2_DRAFT",
    "requires_human_review": True,
    "read_layers": ["case_data"],
    "write_layers": ["case_drafts"],
    "verify_script": "scripts/verify.sh",
    "enabled": True,
    "production_allowed": False,
}


def _write_registry(entries: list[dict]) -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh)
    return path


class TestLoadSkillRegistry:
    def test_load_valid_registry_returns_list(self):
        entries = [dict(VALID_SKILL)]
        path = _write_registry(entries)
        try:
            result = load_skill_registry(path)
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["skill_id"] == "TEST.SKILL_READ"
        finally:
            os.unlink(path)

    def test_load_missing_file_returns_empty_list(self):
        result = load_skill_registry("/nonexistent/skill_registry.json")
        assert result == []


class TestGetSkill:
    def test_get_skill_for_known_skill_returns_dict(self):
        entries = [dict(VALID_SKILL)]
        path = _write_registry(entries)
        try:
            skill = get_skill("TEST.SKILL_READ", path)
            assert isinstance(skill, dict)
            assert skill["skill_id"] == "TEST.SKILL_READ"
            assert skill["skill_name"] == "Test Skill Read"
        finally:
            os.unlink(path)

    def test_get_skill_for_unknown_skill_raises(self):
        entries = [dict(VALID_SKILL)]
        path = _write_registry(entries)
        try:
            with pytest.raises(KeyError, match="Unknown skill"):
                get_skill("NONEXISTENT.SKILL", path)
        finally:
            os.unlink(path)


class TestValidateSkillEntry:
    def test_valid_entry_passes(self):
        result = validate_skill_entry(VALID_SKILL)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_production_allowed_true_is_error(self):
        entry = dict(VALID_SKILL, production_allowed=True)
        result = validate_skill_entry(entry)
        assert result["valid"] is False
        assert any("production_allowed" in e for e in result["errors"])

    def test_write_layers_without_human_review_is_error(self):
        entry = dict(
            VALID_WRITE_SKILL,
            write_layers=["case_drafts"],
            requires_human_review=False,
        )
        result = validate_skill_entry(entry)
        assert result["valid"] is False
        assert any("write_layers" in e for e in result["errors"])

    def test_verify_script_missing_and_risk_r3_is_error(self):
        entry = dict(
            VALID_SKILL,
            risk_level="R3_WRITE_RESEARCH_DB",
            verify_script=None,
        )
        result = validate_skill_entry(entry)
        assert result["valid"] is False
        assert any("verify_script" in e for e in result["errors"])

    def test_disabled_skill_is_error(self):
        entry = dict(VALID_SKILL, enabled=False)
        result = validate_skill_entry(entry)
        assert result["valid"] is False
        assert any("disabled" in e for e in result["errors"])


class TestAssertSkillCallable:
    def test_registered_caller_allowed(self):
        entries = [dict(VALID_SKILL)]
        path = _write_registry(entries)
        try:
            result = assert_skill_callable("z-orchestrator", "TEST.SKILL_READ", path)
            assert result["allowed"] is True
            assert result["reason"] == ""
        finally:
            os.unlink(path)

    def test_unauthorized_caller_not_allowed(self):
        entries = [dict(VALID_SKILL)]
        path = _write_registry(entries)
        try:
            result = assert_skill_callable("unknown-agent", "TEST.SKILL_READ", path)
            assert result["allowed"] is False
            assert "not in allowed_callers" in result["reason"]
        finally:
            os.unlink(path)

    def test_disabled_skill_not_allowed(self):
        entries = [dict(VALID_SKILL, enabled=False)]
        path = _write_registry(entries)
        try:
            result = assert_skill_callable("z-orchestrator", "TEST.SKILL_READ", path)
            assert result["allowed"] is False
            assert "disabled" in result["reason"].lower()
        finally:
            os.unlink(path)

    def test_production_allowed_skill_not_allowed(self):
        entries = [dict(VALID_SKILL, production_allowed=True)]
        path = _write_registry(entries)
        try:
            result = assert_skill_callable("z-orchestrator", "TEST.SKILL_READ", path)
            assert result["allowed"] is False
            assert "production_allowed" in result["reason"]
        finally:
            os.unlink(path)
