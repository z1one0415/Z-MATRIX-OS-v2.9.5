"""Physical Signal Schema v1.2 — STUB_ONLY"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class PhysicalSignal:
    signal_id: str
    ticker: str = ""
    signal_type: str = ""
    detected_at: str = ""
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

def validate_signal(signal: dict) -> dict:
    errors = []
    if not signal.get("evidence_hash"):
        errors.append("evidence_hash required")
    if signal.get("production_allowed"):
        errors.append("production_allowed must be false")
    if signal.get("trade_allowed"):
        errors.append("trade_allowed must be false")
    if signal.get("external_api_used"):
        errors.append("external_api_used must be false")
    return {"valid": len(errors) == 0, "errors": errors}
