# allowlist: forbidden-token-definition
"""Skill Registry — dataclass, load/validate/assert functions"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


SKILL_REGISTRY_PATH = os.environ.get(
    "Z_SKILL_REGISTRY_PATH",
    str(Path(__file__).resolve().parent.parent.parent
        / "data" / "research_db" / "agent" / "registry" / "skill_registry.json"),
)


_RISK_ORDER = {
    "R0_READ": 0,
    "R1_ANNOTATE": 1,
    "R2_DRAFT": 2,
    "R3_WRITE_RESEARCH_DB": 3,
    "R4_CODE_PATCH_PROPOSAL": 4,
    "R5_RELEASE_PROPOSAL": 5,
    "R9_FORBIDDEN": 9,
}


def _risk_numeric(level: str) -> int:
    return _RISK_ORDER.get(level, 0)


@dataclass
class SkillRegistryEntry:
    skill_id: str
    skill_name: str
    domain: str
    version: str
    input_schema_ref: str
    output_schema_ref: str
    allowed_callers: list[str] = field(default_factory=list)
    risk_level: str = "R0_READ"
    requires_human_review: bool = False
    read_layers: list[str] = field(default_factory=list)
    write_layers: list[str] = field(default_factory=list)
    verify_script: str | None = None
    enabled: bool = True
    production_allowed: bool = False


def load_skill_registry(path: str | None = None) -> list[dict]:
    if path is None:
        path = os.environ.get("Z_SKILL_REGISTRY_PATH", SKILL_REGISTRY_PATH)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        return []
    return data


def get_skill(skill_id: str, path: str | None = None) -> dict:
    registry = load_skill_registry(path)
    for entry in registry:
        if entry.get("skill_id") == skill_id:
            return entry
    raise KeyError(f"Unknown skill: {skill_id}")


def validate_skill_entry(skill: dict) -> dict:
    errors: list[str] = []

    if skill.get("enabled") is False:
        errors.append("Skill is disabled")

    if skill.get("production_allowed") is True:
        errors.append("production_allowed must be false")

    write_layers = skill.get("write_layers", [])
    requires_review = skill.get("requires_human_review", False)
    if write_layers and not requires_review:
        errors.append(
            "human review required when skill has write_layers"
        )

    risk_level = skill.get("risk_level", "R0_READ")
    verify_script = skill.get("verify_script")
    if verify_script is None and _risk_numeric(risk_level) >= 3:
        errors.append(
            "verify_script missing and risk_level>=R3"
        )

    return {"valid": len(errors) == 0, "errors": errors}


def assert_skill_callable(agent_id: str, skill_id: str, path: str | None = None) -> dict:
    skill = get_skill(skill_id, path)

    if skill.get("enabled") is not True:
        return {"allowed": False, "reason": "Skill is disabled"}

    if skill.get("production_allowed") is True:
        return {"allowed": False, "reason": "production_allowed must be false"}

    allowed_callers = skill.get("allowed_callers", [])
    if agent_id not in allowed_callers:
        return {
            "allowed": False,
            "reason": f"Agent '{agent_id}' not in allowed_callers for skill '{skill_id}'",
        }

    return {"allowed": True, "reason": ""}
