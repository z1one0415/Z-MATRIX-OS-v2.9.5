"""Narrative Event Schema v1.2 — STUB_ONLY"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class NarrativeEvent:
    event_id: str
    ticker: str = ""
    title: str = ""
    body: str = ""
    source_id: str = ""
    source_health_ref: str = ""
    attribution_ref: str = ""
    layer_version_ref: str = ""
    evidence_hash: str = ""
    quality_status: str = "STUB"
    human_review_required: bool = True
    production_allowed: bool = False
    trade_allowed: bool = False
    external_api_used: bool = False
    shadowbroker_deployed: bool = False

def validate_narrative_event(event: dict) -> dict:
    errors = []
    if not event.get("evidence_hash"):
        errors.append("evidence_hash required")
    if event.get("production_allowed"):
        errors.append("production_allowed must be false")
    return {"valid": len(errors) == 0, "errors": errors}
