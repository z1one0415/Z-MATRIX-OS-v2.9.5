#!/usr/bin/env python3
"""Z-Agent Kernel — Command Envelope v0.5.0"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AgentCommandEnvelope:
    command_id: str
    agent_id: str
    command_type: str
    created_at: str = ""
    requested_skill: str = ""
    input_refs: list[str] = field(default_factory=list)
    target_layers: list[str] = field(default_factory=list)
    requested_action: str = ""
    risk_level: str = "R0_READ"
    idempotency_key: str = ""
    dry_run: bool = True
    requires_human_review: bool = True
    production_allowed: bool = False


def create_command_envelope(payload: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    envelope: dict[str, Any] = {
        "command_id": payload.get("command_id", str(uuid.uuid4())),
        "agent_id": payload.get("agent_id", ""),
        "command_type": payload.get("command_type", ""),
        "created_at": payload.get("created_at", now),
        "requested_skill": payload.get("requested_skill", ""),
        "input_refs": payload.get("input_refs", []),
        "target_layers": payload.get("target_layers", []),
        "requested_action": payload.get("requested_action", ""),
        "risk_level": payload.get("risk_level", "R0_READ"),
        "idempotency_key": payload.get("idempotency_key", str(uuid.uuid4())),
        "dry_run": payload.get("dry_run", True),
        "requires_human_review": payload.get("requires_human_review", True),
        "production_allowed": payload.get("production_allowed", False),
    }
    return envelope


def validate_command_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    if not envelope.get("agent_id"):
        errors.append("agent_id must be non-empty")
    if not envelope.get("requested_skill"):
        errors.append("requested_skill must be non-empty")
    if envelope.get("production_allowed"):
        errors.append("production_allowed must be false")
    if envelope.get("risk_level") == "R9_FORBIDDEN":
        errors.append("R9_FORBIDDEN risk_level is directly REJECTED")

    return {"valid": len(errors) == 0, "errors": errors}


def calculate_command_digest(envelope: dict[str, Any]) -> str:
    serialized = json.dumps(envelope, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()[:16]
