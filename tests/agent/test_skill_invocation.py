# allowlist: forbidden-token-definition
"""Tests for skill_invocation — invoke_skill"""
from __future__ import annotations

import json
import os
import tempfile

from zmatrix.agent.skill_invocation import invoke_skill


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


def _write_registry(entries: list[dict]) -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh)
    return path


class TestInvokeSkill:
    def test_invoke_skill_with_valid_command_returns_structured_result(self):
        path = _write_registry([dict(VALID_SKILL)])
        try:
            original_env = os.environ.get("Z_SKILL_REGISTRY_PATH")
            os.environ["Z_SKILL_REGISTRY_PATH"] = path

            command = {
                "command_id": "cmd-1",
                "agent_id": "z-orchestrator",
                "requested_skill": "TEST.SKILL_READ",
            }
            result = invoke_skill(command, {})
            assert isinstance(result, dict)
            assert result["skill_id"] == "TEST.SKILL_READ"
            assert result["status"] in ("DRAFT_CREATED", "EXECUTED", "BLOCKED", "DEGRADED", "DATA_INSUFFICIENT")
        finally:
            os.unlink(path)
            if original_env is not None:
                os.environ["Z_SKILL_REGISTRY_PATH"] = original_env
            else:
                os.environ.pop("Z_SKILL_REGISTRY_PATH", None)

    def test_result_contains_no_buy_sell_strings(self):
        path = _write_registry([dict(VALID_SKILL)])
        try:
            original_env = os.environ.get("Z_SKILL_REGISTRY_PATH")
            os.environ["Z_SKILL_REGISTRY_PATH"] = path

            command = {
                "command_id": "cmd-1",
                "agent_id": "z-orchestrator",
                "requested_skill": "TEST.SKILL_READ",
            }
            result = invoke_skill(command, {})
            result_str = str(result).upper()
            assert "BUY" not in result_str
            assert "SELL" not in result_str
            assert "AUTO_EXECUTE" not in result_str
        finally:
            os.unlink(path)
            if original_env is not None:
                os.environ["Z_SKILL_REGISTRY_PATH"] = original_env
            else:
                os.environ.pop("Z_SKILL_REGISTRY_PATH", None)

    def test_result_has_production_allowed_false(self):
        path = _write_registry([dict(VALID_SKILL)])
        try:
            original_env = os.environ.get("Z_SKILL_REGISTRY_PATH")
            os.environ["Z_SKILL_REGISTRY_PATH"] = path

            command = {
                "command_id": "cmd-1",
                "agent_id": "z-orchestrator",
                "requested_skill": "TEST.SKILL_READ",
            }
            result = invoke_skill(command, {})
            assert result["production_allowed"] is False
        finally:
            os.unlink(path)
            if original_env is not None:
                os.environ["Z_SKILL_REGISTRY_PATH"] = original_env
            else:
                os.environ.pop("Z_SKILL_REGISTRY_PATH", None)

    def test_unknown_skill_returns_blocked_status(self):
        path = _write_registry([dict(VALID_SKILL)])
        try:
            original_env = os.environ.get("Z_SKILL_REGISTRY_PATH")
            os.environ["Z_SKILL_REGISTRY_PATH"] = path

            command = {
                "command_id": "cmd-1",
                "agent_id": "z-orchestrator",
                "requested_skill": "UNKNOWN.SKILL",
            }
            result = invoke_skill(command, {})
            assert result["status"] == "BLOCKED"
            assert "Unknown skill" in result["blocked_reason"]
        finally:
            os.unlink(path)
            if original_env is not None:
                os.environ["Z_SKILL_REGISTRY_PATH"] = original_env
            else:
                os.environ.pop("Z_SKILL_REGISTRY_PATH", None)

    def test_result_has_all_required_fields(self):
        path = _write_registry([dict(VALID_SKILL)])
        try:
            original_env = os.environ.get("Z_SKILL_REGISTRY_PATH")
            os.environ["Z_SKILL_REGISTRY_PATH"] = path

            command = {
                "command_id": "cmd-1",
                "agent_id": "z-orchestrator",
                "requested_skill": "TEST.SKILL_READ",
            }
            result = invoke_skill(command, {})
            required = {"skill_id", "status", "output_ref", "evidence_refs", "quality_status", "blocked_reason", "human_review_required", "production_allowed"}
            assert required <= result.keys()
        finally:
            os.unlink(path)
            if original_env is not None:
                os.environ["Z_SKILL_REGISTRY_PATH"] = original_env
            else:
                os.environ.pop("Z_SKILL_REGISTRY_PATH", None)

    def test_write_layer_skill_sets_human_review_required(self):
        write_skill = {
            "skill_id": "TEST.WRITE",
            "skill_name": "Write Skill",
            "domain": "AUTOCASEFORGE",
            "version": "1.0",
            "input_schema_ref": "w_schema",
            "output_schema_ref": "w_output_schema",
            "allowed_callers": ["z-orchestrator"],
            "risk_level": "R2_DRAFT",
            "requires_human_review": False,
            "read_layers": [],
            "write_layers": ["case_drafts"],
            "verify_script": "scripts/verify.sh",
            "enabled": True,
            "production_allowed": False,
        }
        path = _write_registry([write_skill])
        try:
            original_env = os.environ.get("Z_SKILL_REGISTRY_PATH")
            os.environ["Z_SKILL_REGISTRY_PATH"] = path

            command = {
                "command_id": "cmd-1",
                "agent_id": "z-orchestrator",
                "requested_skill": "TEST.WRITE",
            }
            result = invoke_skill(command, {})
            assert result["human_review_required"] is True
            assert result["status"] == "DRAFT_CREATED"
        finally:
            os.unlink(path)
            if original_env is not None:
                os.environ["Z_SKILL_REGISTRY_PATH"] = original_env
            else:
                os.environ.pop("Z_SKILL_REGISTRY_PATH", None)
