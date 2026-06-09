from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import FORBIDDEN_BRIDGE_OUTPUTS


class A1FactorBridgeDecision(Enum):
    ALLOW_BRIDGE_READONLY_CONTEXT = "ALLOW_BRIDGE_READONLY_CONTEXT"
    ALLOW_BRIDGE_EVIDENCE_SUMMARY = "ALLOW_BRIDGE_EVIDENCE_SUMMARY"
    DENY_BRIDGE_SOURCE_FORBIDDEN = "DENY_BRIDGE_SOURCE_FORBIDDEN"
    DENY_BRIDGE_REAL_SOURCE_FORBIDDEN = "DENY_BRIDGE_REAL_SOURCE_FORBIDDEN"
    DENY_BRIDGE_OUTPUTS_UNSAFE = "DENY_BRIDGE_OUTPUTS_UNSAFE"
    DENY_BRIDGE_EXECUTION_FORBIDDEN = "DENY_BRIDGE_EXECUTION_FORBIDDEN"
    DENY_BRIDGE_FACTOR_DENIED = "DENY_BRIDGE_FACTOR_DENIED"
    DISABLED_DEFAULT_NOOP = "DISABLED_DEFAULT_NOOP"


@dataclass(frozen=True)
class A1FactorBridgeRequest:
    request_id: str = ""
    factor_id: str | None = None
    intent: str = "BRIDGE_READONLY_CONTEXT"
    execution_requested: bool = False
    source_class: str = ""


@dataclass(frozen=True)
class A1FactorBridgeResponse:
    response_id: str = ""
    decision: A1FactorBridgeDecision = field(
        default_factory=lambda: A1FactorBridgeDecision.DISABLED_DEFAULT_NOOP
    )
    evidence: Any = field(default_factory=dict)
    forbidden_outputs_removed: list = field(
        default_factory=lambda: list(FORBIDDEN_BRIDGE_OUTPUTS)
    )
    degraded: bool = True
    mode: str = "DISABLED_DEFAULT_P0"
    bridge_enabled: bool = False
    runtime_enabled: bool = False
    adapter_execution_enabled: bool = False
    capability_execution_enabled: bool = False


@dataclass(frozen=True)
class A1FactorBridgeContext:
    factor_id: str = ""
    source_class: str = ""
    no_real_source_flag: bool = True
    fixture_source_commit: str = "P1_FIXTURE_ONLY"
    decision: Any = field(
        default_factory=lambda: A1FactorBridgeDecision.DISABLED_DEFAULT_NOOP
    )
    forbidden_outputs_removed: list = field(
        default_factory=lambda: list(FORBIDDEN_BRIDGE_OUTPUTS)
    )
    evidence: Any = field(default_factory=dict)


@dataclass(frozen=True)
class A1FactorBridgeEvidence:
    source_commit: str = ""
    source_class: str = "factor_library_fixture"
    no_real_source_flag: bool = True
    fixture_source_commit: str = "P1_FIXTURE_ONLY"
    request_hash: str = ""
    response_hash_placeholder: str = ""
    factor_decision_hash: str = ""
    bridge_decision_hash: str = ""
    permission_tier: str = "T0"
    forbidden_outputs_removed_hash: str = ""
    rollback_marker: bool = False
    privacy_marker: bool = True
    c1_handoff_marker: bool = True


@dataclass(frozen=True)
class A1DeniedFactorContext:
    factor_id: str = ""
    original_decision: str = ""
    reason: str = ""


@dataclass(frozen=True)
class A1BridgeSourceSummary:
    source_class: str = ""
    total_responses: int = 0
    allowed: int = 0
    denied: int = 0
