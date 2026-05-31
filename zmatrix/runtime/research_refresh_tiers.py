"""Research Refresh Tiers v1.2 — fast/slow/heavy layer classification"""
from __future__ import annotations

FAST_RESEARCH_LAYER = [
    "MARKET_OUTCOME_LAYER",
    "ACCOUNT_TRUTH_LAYER",
    "ZC35_CATALYST_LAYER",
]

SLOW_RESEARCH_LAYER = [
    "B_MATRIX_SNAPSHOT_LAYER",
    "NARRATIVE_EVENT_LAYER",
    "PHYSICAL_SIGNAL_LAYER",
    "D_MATRIX_EVENT_LAYER",
    "FACTOR_REGISTRY_LAYER",
]

HEAVY_SYNTHESIS_LAYER = [
    "AUTOCASEFORGE_LAYER",
    "RESEARCH_ANNOTATION_LAYER",
    "PERSONAL_PROFILE_LAYER",
]

def get_tier(layer_id: str) -> str:
    if layer_id in FAST_RESEARCH_LAYER: return "FAST"
    if layer_id in SLOW_RESEARCH_LAYER: return "SLOW"
    if layer_id in HEAVY_SYNTHESIS_LAYER: return "HEAVY"
    return "UNKNOWN"

def get_layer_tiers() -> dict:
    return {
        "fast": FAST_RESEARCH_LAYER,
        "slow": SLOW_RESEARCH_LAYER,
        "heavy": HEAVY_SYNTHESIS_LAYER,
    }
