"""NPA Score Schema v1.2 — Narrative-Physical-Alignment score"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class NPAScore:
    score_id: str
    ticker: str = ""
    narrative_score: float = 0.0
    physical_score: float = 0.0
    alignment_score: float = 0.0
    confidence: float = 0.0
    quality_status: str = "STUB"
    human_review_required: bool = True
    production_allowed: bool = False
    trade_allowed: bool = False
    external_api_used: bool = False
    shadowbroker_deployed: bool = False

def validate_npa_score(score: dict) -> dict:
    errors = []
    if score.get("production_allowed"):
        errors.append("production_allowed must be false")
    if score.get("trade_allowed"):
        errors.append("trade_allowed must be false")
    return {"valid": len(errors) == 0, "errors": errors}
