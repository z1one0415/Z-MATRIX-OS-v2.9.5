# allowlist: forbidden-token-definition
"""Tests for command_envelope — create, validate, digest"""
from __future__ import annotations

from zmatrix.agent.command_envelope import (
    calculate_command_digest,
    create_command_envelope,
    validate_command_envelope,
)


class TestCreateCommandEnvelope:
    def test_create_valid_envelope_returns_dict_with_command_id(self):
        payload = {
            "agent_id": "z-orchestrator",
            "command_type": "QUERY",
            "requested_skill": "layer_query",
        }
        result = create_command_envelope(payload)
        assert isinstance(result, dict)
        assert "command_id" in result
        assert len(result["command_id"]) > 0

    def test_idempotency_key_preserved(self):
        payload = {
            "agent_id": "z-orchestrator",
            "command_type": "QUERY",
            "requested_skill": "layer_query",
            "idempotency_key": "my-key-42",
        }
        result = create_command_envelope(payload)
        assert result["idempotency_key"] == "my-key-42"


class TestValidateCommandEnvelope:
    def test_valid_envelope_passes(self):
        envelope = {
            "command_id": "cmd-1",
            "agent_id": "z-orchestrator",
            "requested_skill": "layer_query",
            "production_allowed": False,
            "risk_level": "R0_READ",
        }
        result = validate_command_envelope(envelope)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_missing_command_id_returns_validation_error(self):
        envelope = {
            "command_id": "",
            "agent_id": "z-orchestrator",
            "requested_skill": "layer_query",
        }
        result = validate_command_envelope(envelope)
        assert result["valid"] is False
        assert any("command_id" in e for e in result["errors"])

    def test_missing_agent_id_returns_validation_error(self):
        envelope = {
            "command_id": "cmd-1",
            "agent_id": "",
            "requested_skill": "layer_query",
        }
        result = validate_command_envelope(envelope)
        assert result["valid"] is False
        assert any("agent_id" in e for e in result["errors"])

    def test_missing_requested_skill_returns_validation_error(self):
        envelope = {
            "command_id": "cmd-1",
            "agent_id": "z-orchestrator",
            "requested_skill": "",
        }
        result = validate_command_envelope(envelope)
        assert result["valid"] is False
        assert any("requested_skill" in e for e in result["errors"])

    def test_production_allowed_true_returns_validation_error(self):
        envelope = {
            "command_id": "cmd-1",
            "agent_id": "z-orchestrator",
            "requested_skill": "layer_query",
            "production_allowed": True,
        }
        result = validate_command_envelope(envelope)
        assert result["valid"] is False
        assert any("production_allowed" in e for e in result["errors"])

    def test_r9_forbidden_risk_level_direct_reject(self):
        envelope = {
            "command_id": "cmd-1",
            "agent_id": "z-orchestrator",
            "requested_skill": "layer_query",
            "risk_level": "R9_FORBIDDEN",
        }
        result = validate_command_envelope(envelope)
        assert result["valid"] is False
        assert any("R9_FORBIDDEN" in e for e in result["errors"])


class TestCalculateCommandDigest:
    def test_digest_deterministic(self):
        envelope = {
            "command_id": "cmd-1",
            "agent_id": "z-orchestrator",
            "requested_skill": "layer_query",
        }
        d1 = calculate_command_digest(envelope)
        d2 = calculate_command_digest(envelope)
        assert d1 == d2
        assert len(d1) == 64
