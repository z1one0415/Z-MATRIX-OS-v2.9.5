"""ZG16 Skill Router v1.2.1 — full coverage + status semantics"""
from __future__ import annotations

_ROUTE_MAP = {
    # R0_READ
    "ZG16.GET_SOURCE_REGISTRY": "_read_schema",
    "ZG16.GET_EVENT_LAYER_VERSIONS": "_read_schema",
    "ZG16.GET_PHYSICAL_SIGNAL_SCHEMA": "_read_schema",
    "ZG16.GET_NARRATIVE_EVENT_SCHEMA": "_read_schema",
    "ZG16.GET_REALITY_CHECK_SCHEMA": "_read_schema",
    "ZG16.GET_NPA_SCHEMA": "_read_schema",
    "ZG16.GET_HYPOTHESIS_SCHEMA": "_read_schema",
    # R1_ANNOTATE
    "ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE": "_load_signal",
    "ZG16.CALCULATE_NPA_SCORE": "_calc_npa",
    # R2_DRAFT
    "ZG16.CREATE_HYPOTHESIS_DRAFT": "_hypothesis_draft",
    "ZG16.CREATE_RESEARCH_ANNOTATION_DRAFT": "_annotation_draft",
    "ZG16.CREATE_ANALYSIS_ZONE_DRAFT": "_analysis_zone_draft",
    "ZG16.CREATE_CASEFORGE_DRAFT_PROPOSAL": "_caseforge_draft",
}

# R0 read skills → EXECUTED
_READ_SKILLS = {k for k in _ROUTE_MAP if k.startswith("ZG16.GET_")}
# R1 annotate skills → DRAFT_CREATED with ANNOTATION_DRAFT
_R1_SKILLS = {"ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE", "ZG16.CALCULATE_NPA_SCORE"}
# R2 draft skills → DRAFT_CREATED with proposal_required=true
_R2_SKILLS = {k for k in _ROUTE_MAP if k.startswith("ZG16.CREATE_")}


def route_zg16_skill(skill_id: str, command_envelope: dict, context_slice: dict) -> dict:
    if skill_id not in _ROUTE_MAP:
        return _blocked(skill_id, f"Unknown ZG16 skill: {skill_id}")

    is_read = skill_id in _READ_SKILLS
    is_r1 = skill_id in _R1_SKILLS
    is_r2 = skill_id in _R2_SKILLS

    handler = globals().get(_ROUTE_MAP[skill_id])
    if handler is None:
        return _blocked(skill_id, f"ZG16 handler missing: {skill_id}")

    try:
        result = handler(command_envelope, context_slice)
    except Exception as e:
        return _blocked(skill_id, str(e))

    if is_read:
        return _wrap(skill_id, "EXECUTED", "STUB_ONLY", result)
    elif is_r1:
        return _wrap(skill_id, "DRAFT_CREATED", "ANNOTATION_DRAFT", result)
    else:  # R2
        r = _wrap(skill_id, "DRAFT_CREATED", "DRAFT", result)
        r["proposal_required"] = True
        r["closed"] = False
        return r


def _wrap(skill_id, status, quality, output):
    return {
        "skill_id": skill_id, "status": status, "quality_status": quality,
        "output": output, "human_review_required": True,
        "proposal_required": False,
        "production_allowed": False, "external_api_used": False,
        "shadowbroker_deployed": False, "trade_allowed": False,
        "verdict_allowed": False, "token_estimate": 40, "evidence_refs": [],
    }

def _blocked(skill_id, reason):
    return {
        "skill_id": skill_id, "status": "BLOCKED", "quality_status": "REJECTED",
        "output": {}, "blocked_reason": reason, "human_review_required": True,
        "proposal_required": False,
        "production_allowed": False, "external_api_used": False,
        "shadowbroker_deployed": False, "trade_allowed": False,
        "verdict_allowed": False, "token_estimate": 10, "evidence_refs": [],
    }

def _read_schema(env, ctx):
    return {"schema_available": True, "source": "registry"}

def _load_signal(env, ctx):
    from .zg16_skill_wrappers import load_physical_signal_fixture
    return load_physical_signal_fixture(env.get("ticker",""))

def _calc_npa(env, ctx):
    from .event_physical.npa_scorer import calculate_npa
    return calculate_npa(ctx.get("narrative_score",0.5), ctx.get("physical_score",0.5))

def _hypothesis_draft(env, ctx):
    from .zg16_skill_wrappers import create_hypothesis_draft
    return create_hypothesis_draft(ctx.get("hypothesis_type","PHYSICAL_PRE_SIGNAL"), env.get("ticker",""), ctx.get("involved_layers",["physical_signal"]), ctx.get("drivers",["physical-signal"]))

def _annotation_draft(env, ctx):
    from .zg16_skill_wrappers import create_research_annotation_draft
    return create_research_annotation_draft(ctx.get("target_type","TICKER"), ctx.get("target_id",""), ctx.get("category","observation"), ctx.get("title",""), ctx.get("body",""))

def _analysis_zone_draft(env, ctx):
    from .zg16_skill_wrappers import create_analysis_zone_draft
    return create_analysis_zone_draft(ctx.get("zone_type","event"), ctx.get("target_scope",""), ctx.get("title",""), ctx.get("body",""))

def _caseforge_draft(env, ctx):
    from .zg16_skill_wrappers import create_caseforge_draft_proposal
    return create_caseforge_draft_proposal(env.get("ticker",""), ctx.get("hypothesis_id",""), ctx.get("annotation_id",""))


def route_skill(skill_id: str, command_envelope: dict, context_slice: dict) -> dict:
    """Domain router entrypoint for Z-SkillOS compatibility."""
    return route_zg16_skill(skill_id, command_envelope, context_slice)
