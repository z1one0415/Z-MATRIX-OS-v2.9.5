"""Reality Check Schema v1.2 — links narrative events to physical signals"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class RealityCheck:
    check_id: str
    narrative_event_id: str = ""
    physical_signal_id: str = ""
    verdict: str = "INCONCLUSIVE"
    confidence: float = 0.0
    evidence_hash: str = ""
    source_id: str = ""
    source_health_ref: str = ""
    attribution_ref: str = ""
    layer_version_ref: str = ""
    quality_status: str = "STUB"
    human_review_required: bool = True
    production_allowed: bool = False
    trade_allowed: bool = False
    external_api_used: bool = False
    shadowbroker_deployed: bool = False

def validate_reality_check(check: dict) -> dict:
    errors = []
    if not check.get("narrative_event_id"):
        errors.append("narrative_event_id required")
    if check.get("production_allowed"):
        errors.append("production_allowed must be false")
    return {"valid": len(errors) == 0, "errors": errors}
