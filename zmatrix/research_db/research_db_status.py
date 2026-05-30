"""ResearchDB Status — phase tracker and constitution principles."""
from __future__ import annotations
from enum import Enum

PHASE = "Phase 0"
STATUS = "PHASE0_DIRECTORY_FREEZE"


class ConstitutionPrinciple(str, Enum):
    FACT_BEFORE_CONCLUSION = "FACT_BEFORE_CONCLUSION"
    DATA_BEFORE_NARRATIVE = "DATA_BEFORE_NARRATIVE"
    TIMESTAMP_BEFORE_BACKTEST = "TIMESTAMP_BEFORE_BACKTEST"
    EVIDENCE_BEFORE_SCORE = "EVIDENCE_BEFORE_SCORE"
    OUTCOME_BEFORE_PROMOTION = "OUTCOME_BEFORE_PROMOTION"
    SINGLE_CASE_NOT_RULE = "SINGLE_CASE_NOT_RULE"
    SNAPSHOT_NOT_PIT = "SNAPSHOT_NOT_PIT"
    PAPER_NOT_PRODUCTION = "PAPER_NOT_PRODUCTION"
    HUMAN_ABOVE_AUTO = "HUMAN_ABOVE_AUTO"
    ALL_MUTATIONS_AUDITABLE = "ALL_MUTATIONS_AUDITABLE"


CONSTITUTION_PRINCIPLES = [p.value for p in ConstitutionPrinciple]


def get_research_db_status() -> dict:
    """Return current ResearchDB status."""
    return {
        "phase": PHASE,
        "status": STATUS,
        "production_allowed": False,
        "next_phase_allowed": False,
        "human_approval_required": True,
        "principles": CONSTITUTION_PRINCIPLES,
    }
