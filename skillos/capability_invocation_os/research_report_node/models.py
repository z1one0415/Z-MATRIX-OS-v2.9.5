"""Research Report Node data models — frozen dataclasses, no execution."""

from dataclasses import dataclass, field
from enum import Enum

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)


class ResearchReportDecision(Enum):
    ALLOW_Z2_READONLY_REPORT = "ALLOW_Z2_READONLY_REPORT"
    ALLOW_Z2_DEGRADED_REPORT = "ALLOW_Z2_DEGRADED_REPORT"
    DENY_Z2_SOURCE_FORBIDDEN = "DENY_Z2_SOURCE_FORBIDDEN"
    DENY_Z2_REAL_SOURCE_FORBIDDEN = "DENY_Z2_REAL_SOURCE_FORBIDDEN"
    DENY_Z2_OUTPUTS_UNSAFE = "DENY_Z2_OUTPUTS_UNSAFE"
    DENY_Z2_GRAPH_DENIED = "DENY_Z2_GRAPH_DENIED"
    DENY_Z2_EVIDENCE_INCOMPLETE = "DENY_Z2_EVIDENCE_INCOMPLETE"
    DENY_Z2_EXECUTION_FORBIDDEN = "DENY_Z2_EXECUTION_FORBIDDEN"
    DISABLED_DEFAULT_NOOP = "DISABLED_DEFAULT_NOOP"


@dataclass(frozen=True)
class ResearchReportNodeRequest:
    request_id: str = ""
    intent: str = "Z2_READONLY_REPORT"
    execution_requested: bool = False


@dataclass(frozen=True)
class ResearchReportNodeResponse:
    response_id: str = ""
    decision: ResearchReportDecision = field(
        default_factory=lambda: ResearchReportDecision.DISABLED_DEFAULT_NOOP
    )
    evidence: dict = field(default_factory=dict)
    sections: list = field(default_factory=list)
    forbidden_outputs_removed: list = field(
        default_factory=lambda: sorted(FORBIDDEN_REPORT_OUTPUTS)
    )
    degraded: bool = True
    mode: str = "DISABLED_DEFAULT_P0"
    report_enabled: bool = False
    runtime_enabled: bool = False
    adapter_execution_enabled: bool = False
    capability_execution_enabled: bool = False
    readonly_only: bool = True
    no_alpha_claim: bool = True
    no_trade_signal: bool = True
    no_position_weight: bool = True


@dataclass(frozen=True)
class ResearchReportSection:
    section_id: str = ""
    section_type: str = ""
    source_refs: list = field(default_factory=list)
    evidence_refs: list = field(default_factory=list)
    confidence_level: str = "LOW"
    degradation_status: str = ""
    blocked_outputs_removed: list = field(default_factory=list)
    readonly_only: bool = True
    no_alpha_claim: bool = True
    no_trade_signal: bool = True


@dataclass(frozen=True)
class ResearchReportEvidence:
    source_class: str = ""
    no_real_source_flag: bool = True
    fixture_source_commit: str = ""
    request_hash: str = ""
    response_hash_placeholder: str = ""
    factor_decision_hash: str = ""
    bridge_decision_hash: str = ""
    graph_node_hash: str = ""
    graph_edge_hash: str = ""
    permission_tier: str = "T0"
    forbidden_outputs_removed_hash: str = ""
    rollback_marker: bool = False
    privacy_marker: bool = True
    c1_handoff_marker: bool = True
    z2_report_node_hash: str = ""
    z2_report_section_hash: str = ""
    z2_report_evidence_hash: str = ""


@dataclass(frozen=True)
class Z9ReviewSnapshotCandidate:
    report_node_id: str = ""
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
    no_trade_result: bool = True
    no_paper_trading: bool = True
    no_broker_action: bool = True
    no_position_change: bool = True


@dataclass(frozen=True)
class ResearchReportSummary:
    source_class: str = ""
    total_sections: int = 0
    allowed: int = 0
    degraded: int = 0
    denied: int = 0


@dataclass(frozen=True)
class ReportDegradationStatus:
    status: str = ""
    reason: str = ""
    severity: str = ""
