# allowlist: forbidden-token-definition
"""Agent Command Envelope — envelope dataclass, create/validate/digest v0.5.1"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ActionIntent(str, Enum):
    QUERY = "QUERY"
    READ = "READ"
    DRAFT_WRITE = "DRAFT_WRITE"
    PROPOSAL = "PROPOSAL"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    AUDIT_READ = "AUDIT_READ"
    REVIEW = "REVIEW"


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
    action_intent: str = "QUERY"
    risk_level: str = "R0_READ"
    idempotency_key: str = ""
    dry_run: bool = True
    requires_human_review: bool = True
    production_allowed: bool = False


def classify_action_intent(requested_action: str) -> str:
    """Classify requested_action string into ActionIntent. EXECUTE checks before PROPOSAL to avoid PATCH ambiguity."""
    ua = requested_action.upper()
    if any(kw in ua for kw in ("EXECUTE", "RUN", "APPLY")):
        return ActionIntent.EXECUTE
    if any(kw in ua for kw in ("PROPOSAL", "CREATE_PATCH")):
        return ActionIntent.PROPOSAL
    if any(kw in ua for kw in ("VERIFY", "CHECK", "VALIDATE")):
        return ActionIntent.VERIFY
    if any(kw in ua for kw in ("DRAFT", "WRITE", "CREATE_DRAFT")):
        return ActionIntent.DRAFT_WRITE
    if any(kw in ua for kw in ("READ", "FETCH", "GET")):
        return ActionIntent.READ
    if any(kw in ua for kw in ("QUERY", "LIST", "SUMMARY")):
        return ActionIntent.QUERY
    if any(kw in ua for kw in ("AUDIT", "INSPECT")):
        return ActionIntent.AUDIT_READ
    if any(kw in ua for kw in ("REVIEW", "ASSESS")):
        return ActionIntent.REVIEW
    return ActionIntent.QUERY


def create_command_envelope(payload: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    command_id = payload.get("command_id") or str(uuid.uuid4())
    idempotency_key = payload.get("idempotency_key") or command_id
    action = payload.get("requested_action", "")
    intent = payload.get("action_intent", classify_action_intent(action))

    envelope = {
        "command_id": command_id,
        "agent_id": payload.get("agent_id", ""),
        "command_type": payload.get("command_type", ""),
        "created_at": payload.get("created_at", now),
        "requested_skill": payload.get("requested_skill", ""),
        "input_refs": payload.get("input_refs", []),
        "target_layers": payload.get("target_layers", []),
        "requested_action": action,
        "action_intent": intent,
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

    # Validate action_intent alignment
    intent = envelope.get("action_intent", "QUERY")
    action = envelope.get("requested_action", "")
    classified = classify_action_intent(action)
    if intent != classified and action:
        errors.append(f"action_intent {intent} mismatch with action '{action}' (classified {classified})")

    return {"valid": len(errors) == 0, "errors": errors}


def calculate_command_digest(envelope: dict) -> str:
    canonical = json.dumps(envelope, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
