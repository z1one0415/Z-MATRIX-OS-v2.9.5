"""ResearchDB Promotion Policy — case-to-rule progression enforcement."""
from __future__ import annotations
from enum import Enum


class PromotionLevel(str, Enum):
    RAW_DATA = "RAW_DATA"
    FORMAT_VALIDATED = "FORMAT_VALIDATED"
    SOURCE_VALIDATED = "SOURCE_VALIDATED"
    CROSS_SOURCE_VALIDATED = "CROSS_SOURCE_VALIDATED"
    OUTCOME_VALIDATED = "OUTCOME_VALIDATED"
    RESEARCH_ACCEPTED = "RESEARCH_ACCEPTED"
    PAPER_RULE_CANDIDATE = "PAPER_RULE_CANDIDATE"


def case_to_rule_level(case_count: int, cross_ticker: bool = False,
                       cross_regime: bool = False) -> str:
    """Determine the rule level from case evidence count.

    Args:
        case_count: Number of similar cases.
        cross_ticker: Whether cases span multiple tickers.
        cross_regime: Whether cases span multiple market regimes.

    Returns:
        String: LESSON_ONLY, RULE_CANDIDATE, RESEARCH_RULE, or PAPER_RULE.
    """
    if case_count < 3:
        return "LESSON_ONLY"
    if case_count < 10:
        return "RULE_CANDIDATE"
    if case_count >= 20 and cross_ticker and cross_regime:
        return "PAPER_RULE"
    if case_count >= 10 and cross_ticker:
        return "RESEARCH_RULE"
    return "RULE_CANDIDATE"


def can_promote(current_level: PromotionLevel, target_level: PromotionLevel) -> bool:
    """Check if promotion from current to target level is valid (no skipping)."""
    levels = list(PromotionLevel)
    if current_level not in levels or target_level not in levels:
        return False
    current_idx = levels.index(current_level)
    target_idx = levels.index(target_level)
    return target_idx == current_idx + 1  # Only one step at a time
