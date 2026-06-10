"""Z9 Review Node data models — frozen dataclasses, no execution."""

from dataclasses import dataclass, field
from enum import Enum

from skillos.capability_invocation_os.review_node.constants import (
    FORBIDDEN_OUTPUT_KEYS,
)


class Z9ReviewDecision(Enum):
    ALLOW_Z9_READONLY_REVIEW = "ALLOW_Z9_READONLY_REVIEW"
    ALLOW_Z9_DEGRADED_REVIEW = "ALLOW_Z9_DEGRADED_REVIEW"
    DENY_Z9_SOURCE_FORBIDDEN = "DENY_Z9_SOURCE_FORBIDDEN"
    DENY_Z9_REAL_SOURCE_FORBIDDEN = "DENY_Z9_REAL_SOURCE_FORBIDDEN"
    DENY_Z9_OUTPUTS_UNSAFE = "DENY_Z9_OUTPUTS_UNSAFE"
    DENY_Z9_TRADE_RESULT_FORBIDDEN = "DENY_Z9_TRADE_RESULT_FORBIDDEN"
    DENY_Z9_EVIDENCE_INCOMPLETE = "DENY_Z9_EVIDENCE_INCOMPLETE"
    DENY_Z9_MEMORY_MUTATION_FORBIDDEN = "DENY_Z9_MEMORY_MUTATION_FORBIDDEN"
    DENY_Z9_EXECUTION_FORBIDDEN = "DENY_Z9_EXECUTION_FORBIDDEN"
    DISABLED_DEFAULT_NOOP = "DISABLED_DEFAULT_NOOP"


@dataclass(frozen=True)
class Z9ReviewNodeRequest:
    request_id: str = ""
    intent: str = "Z9_READONLY_REVIEW"
    execution_requested: bool = False
    memory_mutation_requested: bool = False


@dataclass(frozen=True)
class Z9ReviewNodeResponse:
    response_id: str = ""
    decision: Z9ReviewDecision = field(
        default_factory=lambda: Z9ReviewDecision.DISABLED_DEFAULT_NOOP
    )
    evidence: dict = field(default_factory=dict)
    sections: list = field(default_factory=list)
    forbidden_outputs_removed: list = field(
        default_factory=lambda: sorted(FORBIDDEN_OUTPUT_KEYS)
    )
    degraded: bool = True
    mode: str = "DISABLED_DEFAULT_P0"
    review_enabled: bool = False
    runtime_enabled: bool = False
    adapter_execution_enabled: bool = False
    capability_execution_enabled: bool = False
    memory_mutation_enabled: bool = False
    readonly_only: bool = True
    no_trade_result: bool = True
    no_paper_trading: bool = True
    no_broker_action: bool = True
    no_position_change: bool = True


@dataclass(frozen=True)
class Z9ReviewSection:
    section_id: str = ""
    section_type: str = ""
    source_refs: list = field(default_factory=list)
    evidence_refs: list = field(default_factory=list)
    review_label: str = ""
    confidence_alignment_label: str = ""
    degradation_status: str = ""
    blocked_outputs_removed: list = field(default_factory=list)
    readonly_only: bool = True


@dataclass(frozen=True)
class Z9ReviewEvidence:
    source_z2_report_node_id: str = ""
    source_graph_hash: str = ""
    factor_context_summary_hash: str = ""
    evidence_chain_hash: str = ""
    research_summary_hash: str = ""
    risk_warning_hash: str = ""
    confidence_level: str = "LOW"
    confidence_reason: str = ""
    missing_evidence: list = field(default_factory=list)
    degradation_status: str = ""
    blocked_outputs_removed: list = field(default_factory=list)
    review_required: bool = False
    review_reason: str = ""
    readonly_only: bool = True
    z9_review_node_hash: str = ""
    z9_review_section_hash: str = ""
    z9_feedback_candidate_hash: str = ""
    rollback_marker: bool = False
    privacy_marker: bool = True


@dataclass(frozen=True)
class Z2FeedbackCandidate:
    source_z2_report_node_id: str = ""
    review_label: str = ""
    evidence_gap_summary: str = ""
    confidence_alignment_issue: str = ""
    blocked_output_issue: str = ""
    missing_evidence: list = field(default_factory=list)
    recommended_report_revision: str = ""
    next_validation_requirement: str = ""
    readonly_only: bool = True
    requires_human_review: bool = True


@dataclass(frozen=True)
class Z9ReviewDegradationStatus:
    status: str = ""
    reason: str = ""
    severity: str = ""


@dataclass(frozen=True)
class Z9ReviewSummary:
    source_z2_report_node_id: str = ""
    total_sections: int = 0
    allowed: int = 0
    degraded: int = 0
    denied: int = 0
