# allowlist: forbidden-token-definition
"""Skill Invocation — invoke_skill entry point"""
from __future__ import annotations

import uuid

from .command_envelope import validate_command_envelope
from .agent_registry import get_agent
from .agent_permission import evaluate_agent_permission
from .skill_registry import get_skill, assert_skill_callable
from zmatrix.research_db.zg16_skill_router import route_zg16_skill
from .token_budget import enforce_token_budget


_FORBIDDEN_OUTPUT_TOKENS = frozenset({"BUY", "SELL", "AUTO_EXECUTE", "READY_FOR_PRODUCTION"})


def _blocked_result(skill_id: str, reason: str) -> dict:
    return {
        "skill_id": skill_id,
        "status": "BLOCKED",
        "output_ref": "",
        "evidence_refs": [],
        "quality_status": "REJECTED",
        "blocked_reason": reason,
        "human_review_required": True,
        "production_allowed": False,
    }


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

    env_validation = validate_command_envelope(command_envelope)
    if not env_validation["valid"]:
        return _blocked_result(
            skill_id,
            "Invalid command envelope: " + "; ".join(env_validation["errors"]),
        )

    try:
        agent = get_agent(command_envelope.get("agent_id", ""))
    except KeyError as e:
        return _blocked_result(skill_id, str(e))

    perm_result = evaluate_agent_permission(agent, command_envelope)
    if not perm_result["allowed"]:
        return _blocked_result(
            skill_id,
            "Permission denied: " + "; ".join(perm_result["blocked_reasons"]),
        )

    try:
        callable_result = assert_skill_callable(command_envelope.get("agent_id", ""), skill_id)
    except KeyError as e:
        return _blocked_result(skill_id, str(e))
    if not callable_result["allowed"]:
        return _blocked_result(skill_id, callable_result["reason"])

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

    ctx_tokens = context_slice.get("token_estimate", 0)
    budget_result = enforce_token_budget({"token_estimate": ctx_tokens}, 4000)
    if ctx_tokens > 4000:
        return {
            "skill_id": skill_id,
            "status": "BLOCKED",
            "output_ref": "",
            "evidence_refs": [],
            "quality_status": "NEED_NARROWER_QUERY",
            "blocked_reason": "token budget exceeded (max 4000)",
            "human_review_required": True,
            "production_allowed": False,
        }

    # ZG16 skill routing
    if skill_id.startswith("ZG16."):
        zg16_result = route_zg16_skill(skill_id, command_envelope, context_slice)
        zg16_result["evidence_refs"] = []
        if _contains_forbidden_token(zg16_result):
            zg16_result["status"] = "BLOCKED"
            zg16_result["blocked_reason"] = "Output contains forbidden token"
        return zg16_result

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
        "action_intent": command_envelope.get("action_intent", "QUERY"),
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
