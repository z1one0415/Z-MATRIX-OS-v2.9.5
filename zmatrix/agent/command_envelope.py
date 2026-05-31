# allowlist: forbidden-token-definition
"""Agent Command Envelope — envelope dataclass, create/validate/digest"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AgentCommandEnvelope:
    command_id: str
    agent_id: str
    command_type: str
    created_at: str
    requested_skill: str
    input_refs: list[str] = field(default_factory=list)
    target_layers: list[str] = field(default_factory=list)
    requested_action: str = ""
    risk_level: str = "R0_READ"
    idempotency_key: str = ""
    dry_run: bool = True
    requires_human_review: bool = True
    production_allowed: bool = False


def create_command_envelope(payload: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    command_id = payload.get("command_id") or str(uuid.uuid4())
    idempotency_key = payload.get("idempotency_key") or command_id

    envelope = {
        "command_id": command_id,
        "agent_id": payload.get("agent_id", ""),
        "command_type": payload.get("command_type", ""),
        "created_at": payload.get("created_at", now),
        "requested_skill": payload.get("requested_skill", ""),
        "input_refs": payload.get("input_refs", []),
        "target_layers": payload.get("target_layers", []),
        "requested_action": payload.get("requested_action", ""),
        "risk_level": payload.get("risk_level", "R0_READ"),
        "idempotency_key": idempotency_key,
        "dry_run": payload.get("dry_run", True),
        "requires_human_review": payload.get("requires_human_review", True),
        "production_allowed": payload.get("production_allowed", False),
    }
    return envelope


def validate_command_envelope(envelope: dict) -> dict:
    errors: list[str] = []

    if not envelope.get("command_id"):
        errors.append("command_id must be non-empty")

    if not envelope.get("agent_id"):
        errors.append("agent_id must be non-empty")

    if not envelope.get("requested_skill"):
        errors.append("requested_skill must be non-empty")

    if envelope.get("production_allowed") is True:
        errors.append("production_allowed must be false")

    if envelope.get("risk_level") == "R9_FORBIDDEN":
        errors.append("R9_FORBIDDEN risk_level is directly REJECTED")

    return {"valid": len(errors) == 0, "errors": errors}


def calculate_command_digest(envelope: dict) -> str:
    canonical = json.dumps(envelope, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
