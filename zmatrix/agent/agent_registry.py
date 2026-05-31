# allowlist: forbidden-token-definition
"""Agent Registry — enum types, dataclass, load/validate/assert functions"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class AgentType(str, Enum):
    ORCHESTRATOR = "ORCHESTRATOR"
    ENGINEERING = "ENGINEERING"
    RESEARCH = "RESEARCH"
    REPORT_RENDERER = "REPORT_RENDERER"
    FRONTEND_ASSISTANT = "FRONTEND_ASSISTANT"
    MAINTENANCE = "MAINTENANCE"


class AgentPermissionLevel(str, Enum):
    VIEW_ONLY = "VIEW_ONLY"
    ANNOTATION_WRITER = "ANNOTATION_WRITER"
    CASE_DRAFT_WRITER = "CASE_DRAFT_WRITER"
    REPORT_DRAFT_WRITER = "REPORT_DRAFT_WRITER"
    RESEARCH_DB_PROPOSER = "RESEARCH_DB_PROPOSER"
    CODE_PATCH_PROPOSER = "CODE_PATCH_PROPOSER"
    VERIFY_RUNNER = "VERIFY_RUNNER"
    RELEASE_PROPOSER = "RELEASE_PROPOSER"


AGENT_REGISTRY_PATH = os.environ.get(
    "Z_AGENT_REGISTRY_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "registry" / "agent_registry.json"),
)


@dataclass
class AgentRegistryEntry:
    agent_id: str
    agent_name: str
    agent_type: str
    owner: str
    role: str
    permission_level: str
    allowed_scopes: list[str]
    allowed_read_layers: list[str]
    allowed_write_layers: list[str]
    allowed_commands: list[str]
    forbidden_commands: list[str]
    max_risk_level: str
    requires_human_review: bool
    workspace_path: str
    enabled: bool
    created_at: str
    production_allowed: bool = False


_RISK_ORDER = {
    "R0_READ": 0,
    "R1_ANNOTATE": 1,
    "R2_DRAFT": 2,
    "R3_WRITE_RESEARCH_DB": 3,
    "R4_CODE_PATCH_PROPOSAL": 4,
    "R5_RELEASE_PROPOSAL": 5,
    "R9_FORBIDDEN": 9,
}

_HARD_FORBIDDEN_SCOPES = frozenset({("*",), ('*',)})


def _risk_numeric(level: str) -> int:
    return _RISK_ORDER.get(level, 0)


def load_agent_registry(path: str | None = None) -> list[dict]:
    path = path or AGENT_REGISTRY_PATH
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        return []
    return data


def get_agent(agent_id: str, path: str | None = None) -> dict:
    registry = load_agent_registry(path)
    for entry in registry:
        if entry.get("agent_id") == agent_id:
            return entry
    raise KeyError(f"Unknown agent: {agent_id}")


def validate_agent_entry(entry: dict) -> dict:
    errors: list[str] = []

    if entry.get("enabled") is False:
        errors.append("Agent is disabled")

    if entry.get("production_allowed") is True:
        errors.append("production_allowed must be false")

    scopes = entry.get("allowed_scopes", [])
    if tuple(scopes) in _HARD_FORBIDDEN_SCOPES:
        errors.append('allowed_scopes cannot be ["*"] — wildcard scope forbidden')

    requires_review = entry.get("requires_human_review", True)
    max_risk = entry.get("max_risk_level", "R2_DRAFT")
    if requires_review is False and _risk_numeric(max_risk) >= 3:
        errors.append(
            "human review must be true when risk level is R3 or above"
        )

    return {"valid": len(errors) == 0, "errors": errors}


def assert_agent_enabled(agent_id: str, path: str | None = None) -> dict:
    entry = get_agent(agent_id, path)
    if entry.get("enabled") is not True:
        return {"allowed": False, "reason": "Agent is disabled"}
    return {"allowed": True, "reason": ""}


def assert_agent_scope(agent_id: str, scope: str, path: str | None = None) -> dict:
    entry = get_agent(agent_id, path)
    allowed = entry.get("allowed_scopes", [])
    if scope not in allowed:
        return {"allowed": False, "reason": f"Scope '{scope}' not in allowed_scopes"}
    return {"allowed": True, "reason": ""}
