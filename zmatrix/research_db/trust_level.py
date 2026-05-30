"""ResearchDB Data Trust Level — enum and permission functions."""
from __future__ import annotations
from enum import Enum


class DataTrustLevel(str, Enum):
    T0_RAW_IMPORT = "T0_RAW_IMPORT"
    T1_FORMAT_VALIDATED = "T1_FORMAT_VALIDATED"
    T2_SOURCE_VALIDATED = "T2_SOURCE_VALIDATED"
    T3_CROSS_SOURCE_VALIDATED = "T3_CROSS_SOURCE_VALIDATED"
    T4_OUTCOME_VALIDATED = "T4_OUTCOME_VALIDATED"
    T5_RESEARCH_ACCEPTED = "T5_RESEARCH_ACCEPTED"


def can_enter_factor_validation(level: DataTrustLevel) -> bool:
    """T4+ required for factor validation."""
    return level in (DataTrustLevel.T4_OUTCOME_VALIDATED, DataTrustLevel.T5_RESEARCH_ACCEPTED)


def can_enter_research_report(level: DataTrustLevel) -> bool:
    """T2+ required for research report conclusions."""
    return level not in (DataTrustLevel.T0_RAW_IMPORT, DataTrustLevel.T1_FORMAT_VALIDATED)


def can_enter_promotion(level: DataTrustLevel) -> bool:
    """T4+ required for promotion consideration."""
    return level in (DataTrustLevel.T4_OUTCOME_VALIDATED, DataTrustLevel.T5_RESEARCH_ACCEPTED)
