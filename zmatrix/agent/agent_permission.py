#!/usr/bin/env python3
"""Z-Agent Kernel — Agent Permission Gate v0.5.0"""
from __future__ import annotations

from enum import Enum
from typing import Any


class CommandRiskLevel(str, Enum):
    R0_READ = "R0_READ"
    R1_ANNOTATE = "R1_ANNOTATE"
    R2_DRAFT = "R2_DRAFT"
    R3_WRITE_RESEARCH_DB = "R3_WRITE_RESEARCH_DB"
    R4_CODE_PATCH_PROPOSAL = "R4_CODE_PATCH_PROPOSAL"
    R5_RELEASE_PROPOSAL = "R5_RELEASE_PROPOSAL"
    R9_FORBIDDEN = "R9_FORBIDDEN"


_RISK_NUMERIC: dict[str, int] = {
    "R0_READ": 0,
    "R1_ANNOTATE": 1,
    "R2_DRAFT": 2,
    "R3_WRITE_RESEARCH_DB": 3,
    "R4_CODE_PATCH_PROPOSAL": 4,
    "R5_RELEASE_PROPOSAL": 5,
    "R9_FORBIDDEN": 9,
}


def _risk_num(level: str) -> int:
    return _RISK_NUMERIC.get(level, 99)


_PROPOSAL_COMMAND_TYPES = {
    "CREATE_PATCH_PROPOSAL",
    "CREATE_RELEASE_PROPOSAL",
}

_EXECUTION_COMMAND_TYPES = {
    "EXECUTE_PATCH",
    "EXECUTE_RELEASE",
}


def evaluate_agent_permission(agent: dict[str, Any], command: dict[str, Any]) -> dict[str, Any]:
    blocked_reasons: list[str] = []
    allowed = True
    risk_level = command.get("risk_level", "R0_READ")
    command_type = command.get("command_type", "")
    permission_level = agent.get("permission_level", "VIEW_ONLY")
    agent_max_risk = agent.get("max_risk_level", "R0_READ")

    if not agent:
        blocked_reasons.append("unknown agent")
        allowed = False

    if not agent.get("enabled", True):
        blocked_reasons.append("agent disabled")
        allowed = False

    if agent.get("production_allowed"):
        blocked_reasons.append("production_allowed must be false")
        allowed = False

    if risk_level == "R9_FORBIDDEN":
        blocked_reasons.append("R9_FORBIDDEN commands are always blocked")
        allowed = False

    allowed_scopes = agent.get("allowed_scopes", [])
    if allowed_scopes == ["*"]:
        blocked_reasons.append("allowed_scopes cannot be wildcard ['*']")
        allowed = False

    cmd_risk_num = _risk_num(risk_level)
    agent_max_risk_num = _risk_num(agent_max_risk)

    if cmd_risk_num > agent_max_risk_num:
        blocked_reasons.append("command risk exceeds agent max_risk_level")
        allowed = False

    if cmd_risk_num >= 3 and permission_level == "VIEW_ONLY":
        blocked_reasons.append("VIEW_ONLY agent cannot execute R3+ commands")
        allowed = False

    if risk_level in ("R4_CODE_PATCH_PROPOSAL", "R5_RELEASE_PROPOSAL"):
        if command_type in _PROPOSAL_COMMAND_TYPES:
            if allowed and cmd_risk_num <= agent_max_risk_num:
                return {
                    "allowed": True,
                    "risk_level": risk_level,
                    "requires_human_review": True,
                    "route": "PROPOSAL_REQUIRED",
                    "execution_allowed": False,
                    "blocked_reasons": [],
                    "production_allowed": False,
                }
            else:
                blocked_reasons.append("R4/R5 commands require human approval")
                allowed = False
        elif command_type in _EXECUTION_COMMAND_TYPES:
            blocked_reasons.append("R4/R5 execution requires prior approval")
            allowed = False
        else:
            blocked_reasons.append("R4/R5 commands require human approval")
            allowed = False
    elif risk_level in ("R3_WRITE_RESEARCH_DB",):
        if not command.get("requires_human_review", True):
            blocked_reasons.append("R3 requires human review")

    requires_human = True
    if risk_level in ("R0_READ", "R1_ANNOTATE") and not blocked_reasons:
        requires_human = False

    return {
        "allowed": allowed,
        "risk_level": risk_level,
        "requires_human_review": requires_human or bool(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "production_allowed": False,
    }
