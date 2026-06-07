"""
Level 4 internal data models.

These are advisory-internal only. No result_envelope fields.
No caller-visible output fields. No production/broker/real_trade references.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional


class Level4Severity(Enum):
    """Allowed severity levels. BLOCK/FAIL_CLOSED/HARD_STOP excluded."""

    INFO = "info"
    NOTICE = "notice"
    WARN = "warn"
    ESCALATE_REVIEW = "escalate_review"


class Level4Category(Enum):
    """Warning categories from taxonomy policy."""

    SCHEMA_DRIFT = "schema_drift"
    HASH_DRIFT = "hash_drift"
    GOLDEN_MISMATCH = "golden_mismatch"
    SEMANTIC_DRIFT = "semantic_drift"
    RETENTION_BOUND = "retention_bound"
    PRIVACY_REJECTION = "privacy_rejection"
    OBSERVATION_FAILURE = "observation_failure"
    ADAPTER_FAILURE = "adapter_failure"
    CLEANUP_SAFETY = "cleanup_safety"
    LIFECYCLE_INCOMPLETE = "lifecycle_incomplete"


@dataclass(frozen=True)
class Level4EvaluationInput:
    """
    Input to Level 4 evaluation pipeline.

    Must NOT contain raw prompts, user data, broker info, or credentials.
    """
    category: Optional[Level4Category] = None
    evidence_ref: Optional[str] = None
    severity_confidence: Optional[float] = None


@dataclass(frozen=True)
class Level4WarningCandidate:
    """
    A single warning candidate produced by the evaluation.

    NOT written to result_envelope. NOT caller-visible.
    """
    warning_id: str = ""
    category: Optional[Level4Category] = None
    severity: Level4Severity = Level4Severity.INFO
    source_gate: str = ""
    evidence_ref: str = ""
    recommended_action: str = ""


@dataclass(frozen=True)
class Level4EvaluationResult:
    """
    Result of Level 4 evaluation.

    In disabled mode, warnings list is empty and action is CONTINUE.
    Never contains result_envelope fields, caller output, or production data.
    """

    action: str = "CONTINUE"
    warnings: List[Level4WarningCandidate] = field(default_factory=list)
    disabled: bool = True

    def __post_init__(self):
        # Ensure action is always CONTINUE (frozen dataclass)
        object.__setattr__(self, "action", "CONTINUE")
