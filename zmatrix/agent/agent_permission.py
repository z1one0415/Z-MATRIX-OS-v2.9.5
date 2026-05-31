# allowlist: forbidden-token-definition
"""Agent Permission Gate — risk-level enum and permission evaluator"""
from __future__ import annotations

from enum import Enum


class CommandRiskLevel(str, Enum):
    R0_READ = "R0_READ"
    R1_ANNOTATE = "R1_ANNOTATE"
    R2_DRAFT = "R2_DRAFT"
    R3_WRITE_RESEARCH_DB = "R3_WRITE_RESEARCH_DB"
    R4_CODE_PATCH_PROPOSAL = "R4_CODE_PATCH_PROPOSAL"
    R5_RELEASE_PROPOSAL = "R5_RELEASE_PROPOSAL"
    R9_FORBIDDEN = "R9_FORBIDDEN"


_RISK_NUMERIC = {
    "R0_READ": 0,
    "R1_ANNOTATE": 1,
    "R2_DRAFT": 2,
    "R3_WRITE_RESEARCH_DB": 3,
    "R4_CODE_PATCH_PROPOSAL": 4,
    "R5_RELEASE_PROPOSAL": 5,
    "R9_FORBIDDEN": 9,
}


def _risk_num(level: str) -> int:
    return _RISK_NUMERIC.get(level, 0)


def evaluate_agent_permission(agent: dict, command: dict) -> dict:
    blocked_reasons: list[str] = []

    agent_perm = agent.get("permission_level", "VIEW_ONLY")
    agent_max_risk = agent.get("max_risk_level", "R2_DRAFT")
    agent_review = agent.get("requires_human_review", True)

    cmd_risk = command.get("risk_level", "R0_READ")
    cmd_prod_allowed = command.get("production_allowed", False)
    cmd_review = command.get("requires_human_review", True)

    risk_num = _risk_num(cmd_risk)

    if cmd_risk == "R9_FORBIDDEN":
        blocked_reasons.append("R9_FORBIDDEN commands are always blocked")

    if cmd_prod_allowed is True:
        blocked_reasons.append("production_allowed must be false")

    if agent_perm == "VIEW_ONLY" and risk_num >= 3:
        blocked_reasons.append("VIEW_ONLY agent cannot execute R3+ commands")

    if risk_num >= 3:
        if cmd_review is not True or agent_review is not True:
            blocked_reasons.append("R3+ commands require requires_human_review=true on both agent and command")

    if risk_num >= 4:
        blocked_reasons.append("R4/R5 commands require human approval")

    allowed = len(blocked_reasons) == 0
    requires_review = risk_num >= 3 or (agent_review and cmd_review)

    return {
        "allowed": allowed,
        "risk_level": cmd_risk,
        "requires_human_review": requires_review,
        "blocked_reasons": blocked_reasons,
        "production_allowed": cmd_prod_allowed,
    }
