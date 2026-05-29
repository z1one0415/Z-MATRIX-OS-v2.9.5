"""V4.0-C3 Research Council — Scoring Configuration

Each reviewer must have a unique scoring_config dict.
This module provides the type definition and validation utilities.
"""
from __future__ import annotations


# Required keys in every reviewer's scoring_config
REQUIRED_SCORING_KEYS = frozenset({
    "score_min", "score_max", "weights", "thresholds",
})


def validate_scoring_config(config: dict) -> bool:
    """Validate that a scoring_config has required structure."""
    if not config:
        return False
    for key in REQUIRED_SCORING_KEYS:
        if key not in config:
            return False
    score_min = config.get("score_min", 0)
    score_max = config.get("score_max", 100)
    if not (0 <= score_min < score_max <= 100):
        return False
    weights = config.get("weights", {})
    if not isinstance(weights, dict) or not weights:
        return False
    # Weights should be positive
    for k, v in weights.items():
        if not isinstance(v, (int, float)) or v <= 0:
            return False
    thresholds = config.get("thresholds", {})
    if not isinstance(thresholds, dict):
        return False
    return True


def scoring_configs_are_unique(configs: list[dict]) -> bool:
    """Check that no two configs are identical (deep comparison)."""
    import json
    serialized = [json.dumps(c, sort_keys=True) for c in configs]
    return len(set(serialized)) == len(configs)
