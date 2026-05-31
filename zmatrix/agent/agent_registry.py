#!/usr/bin/env python3
"""Z-Agent Kernel — Agent Registry v0.5.0"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


AGENT_REGISTRY_PATH = str(
    Path(__file__).resolve().parent.parent.parent
    / "data/research_db/agent/registry/agent_registry.json"
)


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


@dataclass
class AgentRegistryEntry:
    agent_id: str
    agent_name: str
    agent_type: AgentType
    owner: str = "system"
    role: str = ""
    permission_level: AgentPermissionLevel = AgentPermissionLevel.VIEW_ONLY
    allowed_scopes: list[str] = field(default_factory=list)
    allowed_read_layers: list[str] = field(default_factory=list)
    allowed_write_layers: list[str] = field(default_factory=list)
    allowed_commands: list[str] = field(default_factory=list)
    forbidden_commands: list[str] = field(default_factory=list)
    max_risk_level: str = "R2_DRAFT"
    requires_human_review: bool = True
    workspace_path: str = ""
    enabled: bool = True
    created_at: str = ""
    production_allowed: bool = False


def load_agent_registry(path: str = "") -> list[dict[str, Any]]:
    target = path or AGENT_REGISTRY_PATH
    if not os.path.exists(target):
        return _default_agents()
    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        return _default_agents()
    return data


def _default_agents() -> list[dict[str, Any]]:
    return [
        {
            "agent_id": "z-orchestrator",
            "agent_name": "Z-Orchestrator",
            "agent_type": "ORCHESTRATOR",
            "permission_level": "VIEW_ONLY",
            "allowed_scopes": ["research_summary", "layer_query", "skill_draft"],
            "allowed_read_layers": ["*READ_ONLY_REGISTRY"],
            "allowed_write_layers": [],
            "allowed_commands": ["QUERY", "CREATE_DRAFT_COMMAND"],
            "forbidden_commands": [
                "REAL_TRADE", "BROKER_ORDER", "AUTO_BUY", "AUTO_SELL",
                "PRODUCTION_MUTATION",
            ],
            "max_risk_level": "R2_DRAFT",
            "requires_human_review": True,
            "workspace_path": "runtime/agent_workspace/z-orchestrator",
            "enabled": True,
            "production_allowed": False,
        },
        {
            "agent_id": "openclaw-engineering",
            "agent_name": "OpenClaw Engineering Agent",
            "agent_type": "ENGINEERING",
            "permission_level": "CODE_PATCH_PROPOSER",
            "allowed_scopes": ["code_patch_proposal", "verify_runner"],
            "allowed_read_layers": ["docs", "zmatrix", "tests", "scripts"],
            "allowed_write_layers": [
                "runtime/agent_workspace/openclaw-engineering"
            ],
            "allowed_commands": ["CREATE_PATCH_PROPOSAL", "RUN_VERIFY_DRY"],
            "forbidden_commands": [
                "REAL_TRADE", "BROKER_ORDER", "AUTO_BUY", "AUTO_SELL",
                "DIRECT_MAIN_PUSH", "PRODUCTION_MUTATION",
            ],
            "max_risk_level": "R4_CODE_PATCH_PROPOSAL",
            "requires_human_review": True,
            "workspace_path": "runtime/agent_workspace/openclaw-engineering",
            "enabled": True,
            "production_allowed": False,
        },
    ]


def get_agent(agent_id: str, path: str | None = None) -> dict[str, Any]:
    registry = load_agent_registry(path or AGENT_REGISTRY_PATH)
    for entry in registry:
        if entry.get("agent_id") == agent_id:
            return entry
    return {}


def validate_agent_entry(entry: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if not entry.get("agent_id"):
        errors.append("agent_id required")
    if not entry.get("agent_name"):
        errors.append("agent_name required")
    if entry.get("production_allowed"):
        errors.append("production_allowed must be false")
    scopes = entry.get("allowed_scopes", [])
    if scopes == ["*"]:
        errors.append("allowed_scopes cannot be wildcard ['*']")
    return {"valid": len(errors) == 0, "errors": errors}


def assert_agent_enabled(agent_id: str) -> dict[str, Any]:
    agent = get_agent(agent_id)
    if not agent:
        return {"valid": False, "errors": [f"unknown agent: {agent_id}"]}
    if not agent.get("enabled", True):
        return {"valid": False, "errors": [f"agent disabled: {agent_id}"]}
    return {"valid": True, "errors": []}


def assert_agent_scope(agent_id: str, scope: str) -> dict[str, Any]:
    agent = get_agent(agent_id)
    if not agent:
        return {"valid": False, "errors": [f"unknown agent: {agent_id}"]}
    allowed = agent.get("allowed_scopes", [])
    if scope not in allowed and "all" not in allowed:
        return {"valid": False, "errors": [f"scope {scope} not allowed for {agent_id}"]}
    return {"valid": True, "errors": []}
