"""NPA Scorer v1.2 — Narrative-Physical-Alignment scoring, STUB_ONLY"""
from __future__ import annotations

def calculate_npa(narrative_score: float, physical_score: float) -> dict:
    """Calculate NPA alignment score. Returns structured dict, never trade signal."""
    alignment = 1.0 - abs(narrative_score - physical_score)
    return {
        "narrative_score": narrative_score,
        "physical_score": physical_score,
        "alignment_score": round(alignment, 4),
        "confidence": round(max(0.0, min(alignment, 1.0)), 4),
        "quality_status": "STUB",
        "human_review_required": True,
        "production_allowed": False,
        "trade_allowed": False,
        "external_api_used": False,
        "shadowbroker_deployed": False,
    }
