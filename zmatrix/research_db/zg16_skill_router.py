"""ZG16 Skill Router v1.2 — Agent Kernel compliant skill dispatch"""
from __future__ import annotations

_ROUTE_MAP = {
    "ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE": "_load_signal",
    "ZG16.CALCULATE_NPA_SCORE": "_calc_npa",
    "ZG16.CREATE_HYPOTHESIS_DRAFT": "_hypothesis_draft",
    "ZG16.CREATE_RESEARCH_ANNOTATION_DRAFT": "_annotation_draft",
    "ZG16.CREATE_ANALYSIS_ZONE_DRAFT": "_analysis_zone_draft",
    "ZG16.CREATE_CASEFORGE_DRAFT_PROPOSAL": "_caseforge_draft",
}

def route_zg16_skill(skill_id: str, command_envelope: dict, context_slice: dict) -> dict:
    if skill_id not in _ROUTE_MAP:
        return _blocked(skill_id, f"Unknown ZG16 skill: {skill_id}")

    handler = globals().get(_ROUTE_MAP[skill_id])
    if handler is None:
        return _blocked(skill_id, f"ZG16 handler not found: {skill_id}")

    try:
        result = handler(command_envelope, context_slice)
        return _wrap(skill_id, "EXECUTED", "STUB", result)
    except Exception as e:
        return _blocked(skill_id, str(e))


def _wrap(skill_id, status, quality, output):
    return {
        "skill_id": skill_id, "status": status, "quality_status": quality,
        "output": output, "human_review_required": True,
        "production_allowed": False, "external_api_used": False,
        "shadowbroker_deployed": False, "trade_allowed": False,
        "verdict_allowed": False,
    }

def _blocked(skill_id, reason):
    return {
        "skill_id": skill_id, "status": "BLOCKED", "quality_status": "REJECTED",
        "output": {}, "blocked_reason": reason, "human_review_required": True,
        "production_allowed": False, "external_api_used": False,
        "shadowbroker_deployed": False, "trade_allowed": False,
        "verdict_allowed": False,
    }

def _load_signal(env, ctx):
    from .zg16_skill_wrappers import load_physical_signal_fixture
    return load_physical_signal_fixture(env.get("ticker",""))

def _calc_npa(env, ctx):
    n = ctx.get("narrative_score", 0.5)
    p = ctx.get("physical_score", 0.5)
    from .event_physical.npa_scorer import calculate_npa
    return calculate_npa(n, p)

def _hypothesis_draft(env, ctx):
    from .zg16_skill_wrappers import create_hypothesis_draft
    return create_hypothesis_draft(
        ctx.get("hypothesis_type","PHYSICAL_PRE_SIGNAL"), env.get("ticker",""),
        ctx.get("involved_layers",["physical_signal"]),
        ctx.get("drivers",["physical-signal"]))

def _annotation_draft(env, ctx):
    from .zg16_skill_wrappers import create_research_annotation_draft
    return create_research_annotation_draft(
        ctx.get("target_type","TICKER"), ctx.get("target_id",""),
        ctx.get("category","observation"), ctx.get("title",""), ctx.get("body",""))

def _analysis_zone_draft(env, ctx):
    from .zg16_skill_wrappers import create_analysis_zone_draft
    return create_analysis_zone_draft(
        ctx.get("zone_type","event"), ctx.get("target_scope",""),
        ctx.get("title",""), ctx.get("body",""))

def _caseforge_draft(env, ctx):
    from .zg16_skill_wrappers import create_caseforge_draft_proposal
    return create_caseforge_draft_proposal(
        env.get("ticker",""), ctx.get("hypothesis_id",""), ctx.get("annotation_id",""))
