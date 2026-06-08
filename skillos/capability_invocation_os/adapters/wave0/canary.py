"""Wave0 Canary — plan-only, no execution, no real call."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind, ControlledReadonlyMode, ControlledReadonlyReason, ControlledReadonlyDecision

class CanaryPhase(Enum):
    PHASE_1_SYNTHETIC = "PHASE_1_SYNTHETIC"
    PHASE_2_PROVIDED = "PHASE_2_PROVIDED"
    PHASE_3_SANDBOX = "PHASE_3_SANDBOX"
    EXTERNAL = "EXTERNAL"

@dataclass(frozen=True)
class CanaryPlan:
    phase: CanaryPhase
    sample_size: int = 5
    adapter_kind: Optional[Wave0AdapterKind] = None
    input_kind: ControlledInputKind = ControlledInputKind.SYNTHETIC
    allowed: bool = False
    reason: str = "P0 disabled-default"

def plan_synthetic_canary(adapter_kind: Wave0AdapterKind) -> CanaryPlan:
    return CanaryPlan(phase=CanaryPhase.PHASE_1_SYNTHETIC, sample_size=5, adapter_kind=adapter_kind, input_kind=ControlledInputKind.SYNTHETIC, allowed=False, reason="P0: plan only, no execution")

def plan_provided_input_canary(adapter_kind: Wave0AdapterKind) -> CanaryPlan:
    return CanaryPlan(phase=CanaryPhase.PHASE_2_PROVIDED, sample_size=5, adapter_kind=adapter_kind, input_kind=ControlledInputKind.PROVIDED, allowed=False, reason="P0: plan only, no execution")

def reject_external_source_canary() -> CanaryPlan:
    return CanaryPlan(phase=CanaryPhase.EXTERNAL, allowed=False, reason="External source rejected in P0")

def evaluate_canary_boundary(input_kind: ControlledInputKind) -> ControlledReadonlyDecision:
    if input_kind == ControlledInputKind.EXTERNAL:
        return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP, reason=ControlledReadonlyReason.EXTERNAL_SOURCE_REJECTED)
    if input_kind == ControlledInputKind.GITHUB_METADATA:
        return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP, reason=ControlledReadonlyReason.GITHUB_REJECTED)
    return ControlledReadonlyDecision(mode=ControlledReadonlyMode.CANARY_PLAN_ONLY, reason=ControlledReadonlyReason.DISABLED_DEFAULT)
