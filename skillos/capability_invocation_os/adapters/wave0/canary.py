"""Wave0 Canary — plan-only, no execution, no real call."""
from dataclasses import dataclass
from enum import Enum
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind
from skillos.capability_invocation_os.adapters.wave0.controlled_readonly import ControlledInputKind, ControlledReadonlyMode, ControlledReadonlyReason, ControlledReadonlyDecision

class CanaryPhase(Enum): PHASE_1_SYNTHETIC="PHASE_1_SYNTHETIC"; PHASE_2_PROVIDED="PHASE_2_PROVIDED"; PHASE_3_SANDBOX="PHASE_3_SANDBOX"; EXTERNAL="EXTERNAL"

@dataclass(frozen=True)
class CanaryPlan:
    phase:CanaryPhase; sample_size:int=5; adapter_kind:Wave0AdapterKind=Wave0AdapterKind.REPORT_READING; input_kind:ControlledInputKind=ControlledInputKind.SYNTHETIC; allowed:bool=False; reason:str="P0 disabled-default"

def plan_synthetic_canary(ak): return CanaryPlan(phase=CanaryPhase.PHASE_1_SYNTHETIC,adapter_kind=ak,allowed=False,reason="P0: plan only")
def plan_provided_input_canary(ak): return CanaryPlan(phase=CanaryPhase.PHASE_2_PROVIDED,adapter_kind=ak,allowed=False,reason="P0: plan only")
def reject_external_source_canary(): return CanaryPlan(phase=CanaryPhase.EXTERNAL,allowed=False,reason="External rejected in P0")
def evaluate_canary_boundary(ik):
    if ik==ControlledInputKind.EXTERNAL: return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP,reason=ControlledReadonlyReason.EXTERNAL_SOURCE_REJECTED)
    if ik==ControlledInputKind.GITHUB_METADATA: return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP,reason=ControlledReadonlyReason.GITHUB_REJECTED)
    return ControlledReadonlyDecision(mode=ControlledReadonlyMode.CANARY_PLAN_ONLY,reason=ControlledReadonlyReason.DISABLED_DEFAULT)
