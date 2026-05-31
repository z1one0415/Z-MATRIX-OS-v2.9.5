# allowlist: forbidden-token-definition
"""Skill Invocation — invoke_skill entry point"""
from __future__ import annotations

import uuid

from .skill_registry import get_skill

_FORBIDDEN_OUTPUT_TOKENS = frozenset({"BUY", "SELL", "AUTO_EXECUTE", "READY_FOR_PRODUCTION"})


def _contains_forbidden_token(data: dict, tokens: frozenset[str] | None = None) -> bool:
    tokens = tokens if tokens is not None else _FORBIDDEN_OUTPUT_TOKENS

    def _recurse(obj):
        if isinstance(obj, str):
            upper = obj.upper()
            for tok in tokens:
                if tok.upper() in upper:
                    return True
        elif isinstance(obj, dict):
            for v in obj.values():
                if _recurse(v):
                    return True
        elif isinstance(obj, list):
            for v in obj:
                if _recurse(v):
                    return True
        return False

    return _recurse(data)


def invoke_skill(command_envelope: dict, context_slice: dict) -> dict:
    skill_id = command_envelope.get("requested_skill", "")

    blocked = False
    blocked_reason = ""
    human_review_required = False

    try:
        skill = get_skill(skill_id)
    except KeyError:
        return {
            "skill_id": skill_id,
            "status": "BLOCKED",
            "output_ref": "",
            "evidence_refs": [],
            "quality_status": "REJECTED",
            "blocked_reason": f"Unknown skill: {skill_id}",
            "human_review_required": True,
            "production_allowed": False,
        }

    if skill.get("enabled") is not True:
        return {
            "skill_id": skill_id,
            "status": "BLOCKED",
            "output_ref": "",
            "evidence_refs": [],
            "quality_status": "REJECTED",
            "blocked_reason": f"Skill '{skill_id}' is disabled",
            "human_review_required": True,
            "production_allowed": False,
        }

    if skill.get("production_allowed") is True:
        return {
            "skill_id": skill_id,
            "status": "BLOCKED",
            "output_ref": "",
            "evidence_refs": [],
            "quality_status": "REJECTED",
            "blocked_reason": "production_allowed must be false",
            "human_review_required": True,
            "production_allowed": False,
        }

    write_layers = skill.get("write_layers", [])
    if write_layers:
        human_review_required = True

    output_ref = f"skill://{skill_id}/{uuid.uuid4().hex[:12]}"

    result = {
        "skill_id": skill_id,
        "status": "DRAFT_CREATED",
        "output_ref": output_ref,
        "evidence_refs": [],
        "quality_status": "DRAFT",
        "blocked_reason": "",
        "human_review_required": human_review_required,
        "production_allowed": False,
    }

    if _contains_forbidden_token(result):
        return {
            "skill_id": skill_id,
            "status": "BLOCKED",
            "output_ref": "",
            "evidence_refs": [],
            "quality_status": "REJECTED",
            "blocked_reason": "Output contains forbidden token (BUY/SELL/AUTO_EXECUTE/READY_FOR_PRODUCTION)",
            "human_review_required": True,
            "production_allowed": False,
        }

    return result
