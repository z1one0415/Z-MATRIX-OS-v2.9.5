"""Tests for SkillOS Level 3 telemetry redaction."""

import pytest
from zmatrix.agent.skillos_level3_redaction import redact_telemetry


def test_redaction_allows_contract_fields():
    event = {"event_id": "e1", "skill_id": "S.X", "created_by": "test"}
    result = redact_telemetry(event)
    assert result["event_id"] == "e1"


def test_redaction_rejects_raw_prompt():
    with pytest.raises(ValueError, match="raw_prompt"):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "raw_prompt": "hello"})


def test_redaction_rejects_raw_user_data():
    with pytest.raises(ValueError, match="raw_user_data"):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "raw_user_data": "x"})


def test_redaction_rejects_raw_output_payload():
    with pytest.raises(ValueError, match="raw_output_payload"):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "raw_output_payload": "x"})


def test_redaction_rejects_credentials():
    with pytest.raises(ValueError):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "trading_credentials": "x"})


def test_redaction_rejects_account_id():
    with pytest.raises(ValueError):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "account_id": "x"})


def test_redaction_rejects_broker_id():
    with pytest.raises(ValueError):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "broker_id": "x"})


def test_redaction_rejects_real_trade_payload():
    with pytest.raises(ValueError):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "real_trade_payload": "x"})


def test_redaction_rejects_unknown_fields():
    with pytest.raises(ValueError, match="unknown"):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "random_field": "x"})


def test_redaction_runs_before_write():
    """Redaction rejects before any persistence path is touched."""
    with pytest.raises(ValueError):
        redact_telemetry({"event_id": "e1", "skill_id": "S.X", "production_secret": "x"})
