"""ZG16 Skill Wrappers v1.2 — Agent Kernel compliant, STUB_ONLY"""
from __future__ import annotations

def load_physical_signal_fixture(ticker: str = "") -> dict:
    return {"skill_id":"ZG16.LOAD_PHYSICAL_SIGNAL_FIXTURE","status":"DRAFT_CREATED","quality_status":"STUB","human_review_required":True,"production_allowed":False,"output":{"ticker":ticker,"signals":[],"source":"fixture_only"}}

def calculate_npa_score(narrative_eval: float, physical_eval: float) -> dict:
    from .event_physical.npa_scorer import calculate_npa
    return calculate_npa(narrative_eval, physical_eval)

def create_hypothesis_draft(h_type: str, ticker: str, layers: list, drivers: list) -> dict:
    from .hypothesis.cross_layer_hypothesis_engine import generate_hypothesis
    h = generate_hypothesis(h_type, ticker, layers, drivers)
    h["quality_status"] = "DRAFT"
    return h

def create_research_annotation_draft(target_type, target_id, category, title, body) -> dict:
    from .annotation.research_annotation_store import create_annotation
    return create_annotation(target_type, target_id, category, title, body)

def create_analysis_zone_draft(zone_type, target_scope, title, body) -> dict:
    from .analysis_zone.research_analysis_zone import create_analysis_zone
    return create_analysis_zone(zone_type, target_scope, title, body)

def create_caseforge_draft_proposal(ticker, hypothesis_id, annotation_id) -> dict:
    return {"skill_id":"ZG16.CREATE_CASEFORGE_DRAFT_PROPOSAL","status":"DRAFT_CREATED","quality_status":"STUB","human_review_required":True,"production_allowed":False,"output":{"ticker":ticker,"hypothesis_id":hypothesis_id,"annotation_id":annotation_id,"case_stage":"DRAFT"}}
