# allowlist: forbidden-token-definition
"""Agent Identity — session identity dataclass and helpers"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AgentIdentity:
    agent_id: str
    session_id: str
    started_at: str
    token_usage: int = 0


def create_agent_identity(agent_id: str) -> AgentIdentity:
    return AgentIdentity(
        agent_id=agent_id,
        session_id=str(uuid.uuid4()),
        started_at=datetime.now(timezone.utc).isoformat(),
    )


def get_identity_summary(identity: AgentIdentity) -> dict:
    return {
        "agent_id": identity.agent_id,
        "session_id": identity.session_id,
        "started_at": identity.started_at,
        "token_usage": identity.token_usage,
    }
