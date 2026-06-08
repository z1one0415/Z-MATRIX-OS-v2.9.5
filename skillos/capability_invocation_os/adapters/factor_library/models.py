"""Models — frozen dataclasses, disabled-default, no execution fields."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

class FactorAdapterMode(Enum):
    DISABLED = "DISABLED"
    PLAN_ONLY = "PLAN_ONLY"
    READONLY_DENY = "READONLY_DENY"

class FactorAdapterDecision(Enum):
    ALLOW_REGISTRY_ONLY = "ALLOW_REGISTRY_ONLY"
    ALLOW_EVIDENCE_ONLY = "ALLOW_EVIDENCE_ONLY"
    ALLOW_VALIDATION_SUMMARY = "ALLOW_VALIDATION_SUMMARY"
    ALLOW_GUARDRAIL_SUMMARY = "ALLOW_GUARDRAIL_SUMMARY"
    ALLOW_CANDIDATE_MONITOR = "ALLOW_CANDIDATE_MONITOR"
    ALLOW_READONLY_CONTEXT = "ALLOW_READONLY_CONTEXT"
    ALLOW_COMPOSITION_GRAPH_DRY_PLAN = "ALLOW_COMPOSITION_GRAPH_DRY_PLAN"
    DENY_FACTOR_NOT_FOUND = "DENY_FACTOR_NOT_FOUND"
    DENY_FACTOR_NOT_VALIDATED = "DENY_FACTOR_NOT_VALIDATED"
    DENY_PIT_FAILED = "DENY_PIT_FAILED"
    DENY_COVERAGE_FAILED = "DENY_COVERAGE_FAILED"
    DENY_FAMILY_OVERLAP = "DENY_FAMILY_OVERLAP"
    DENY_GUARDRAIL_FAILED = "DENY_GUARDRAIL_FAILED"
    DENY_PROMOTION_NOT_ALLOWED = "DENY_PROMOTION_NOT_ALLOWED"
    DENY_EXECUTION_FORBIDDEN = "DENY_EXECUTION_FORBIDDEN"
    DISABLED_DEFAULT_NOOP = "DISABLED_DEFAULT_NOOP"

@dataclass(frozen=True)
class FactorManifestView:
    factor_id: str = ""
    factor_name: str = ""
    factor_family_id: str = ""
    factor_status: str = "unknown"
    factor_type: str = "unknown"

@dataclass(frozen=True)
class FactorFamilyProfileView:
    family_id: str = ""
    family_group: str = ""
    orthogonality_required: bool = True
    new_family_requires_review: bool = True

@dataclass(frozen=True)
class FactorValidationSnapshotView:
    coverage_passed: bool = False
    pit_passed: bool = False
    promotion_allowed: bool = False
    alpha_claim_allowed: bool = False
    ready_for_candidate_review: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class FactorGuardrailProfileView:
    required_guardrails: List[str] = field(default_factory=list)
    guardrail_state: str = "not_run"

@dataclass(frozen=True)
class FactorApplicationContractView:
    allowed_application_modes: List[str] = field(default_factory=list)
    blocked_application_modes: List[str] = field(default_factory=lambda: [
        "ALPHA_SIGNAL", "ORDER_SIGNAL", "PORTFOLIO_WEIGHT",
        "PAPER_TRADING", "BROKER_RUNTIME", "REAL_TRADE", "PRODUCTION",
    ])
    blocked_outputs: List[str] = field(default_factory=lambda: [
        "buy_signal", "sell_signal", "position_weight",
        "expected_return_claim", "alpha_claim", "order_signal",
        "broker_runtime", "real_trade", "production",
    ])
    execution_requested: bool = False
    promotion_allowed: bool = False
    alpha_claim_allowed: bool = False

@dataclass(frozen=True)
class FactorEvidenceEnvelopeView:
    source_commit: str = ""
    request_hash: str = ""
    decision_hash: str = ""
    factor_manifest_hash: str = ""
    validation_snapshot_hash: str = ""
    permission_tier: str = "T0"
    source_class: str = "factor_library"
    rollback_marker: bool = False

@dataclass(frozen=True)
class FactorInvocationRequest:
    request_id: str = ""
    intent: str = ""
    factor_selector: Optional[Dict[str, Any]] = None
    execution_requested: bool = False

@dataclass(frozen=True)
class FactorInvocationResponse:
    response_id: str = ""
    decision: FactorAdapterDecision = FactorAdapterDecision.DISABLED_DEFAULT_NOOP
    evidence: Optional[FactorEvidenceEnvelopeView] = None
    forbidden_outputs_removed: List[str] = field(default_factory=lambda: list(BLOCKED_OUTPUTS))
    degraded: bool = True

@dataclass(frozen=True)
class FactorFilter:
    factor_id: Optional[str] = None
    family_id: Optional[str] = None

@dataclass(frozen=True)
class CandidateMonitorRequest:
    candidate_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class CandidateMonitorView:
    candidates: List[Dict[str, Any]] = field(default_factory=list)

@dataclass(frozen=True)
class ResearchContextView:
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class DeniedFactorView:
    factor_id: str = ""
    reason: FactorAdapterDecision = FactorAdapterDecision.DISABLED_DEFAULT_NOOP

from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS
