"""Wave0 Controlled Read-Only Execution — disabled-default P0 control layer.
No execute. No run. No call. No invoke. No real adapter action.
Returns internal decision objects only. DISABLED/DENY_NOOP/PLAN_ONLY/CANARY_PLAN_ONLY."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind

class ControlledReadonlyMode(Enum): DISABLED="DISABLED"; DENY_NOOP="DENY_NOOP"; PLAN_ONLY="PLAN_ONLY"; CANARY_PLAN_ONLY="CANARY_PLAN_ONLY"
class ControlledReadonlyReason(Enum): DISABLED_DEFAULT="P0 disabled-default"; GATE_NOT_REQUESTED="gate not fully requested"; KILL_SWITCH_ACTIVE="kill switch override"; PERMISSION_DENIED="permission check failed"; EXTERNAL_SOURCE_REJECTED="external source not allowed in P0"; GITHUB_REJECTED="GitHub real call not allowed in P0"; ZMATRIX_REJECTED="Z-MATRIX call permanently rejected"
class ControlledInputKind(Enum): SYNTHETIC="SYNTHETIC"; PROVIDED="PROVIDED"; LOCAL_SANDBOX="LOCAL_SANDBOX"; EXTERNAL="EXTERNAL"; GITHUB_METADATA="GITHUB_METADATA"

@dataclass(frozen=True)
class ControlledReadonlyRequest: adapter_kind:Wave0AdapterKind=Wave0AdapterKind.GITHUB_READONLY; input_kind:ControlledInputKind=ControlledInputKind.SYNTHETIC; requested:bool=False

@dataclass(frozen=True)
class ControlledReadonlyDecision:
    mode:ControlledReadonlyMode=ControlledReadonlyMode.DISABLED; reason:ControlledReadonlyReason=ControlledReadonlyReason.DISABLED_DEFAULT
    adapter_kind:Optional[Wave0AdapterKind]=None; input_kind:Optional[ControlledInputKind]=None

def plan_controlled_readonly_execution(cfg, adapter_kind, input_kind):
    from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
    if input_kind in (ControlledInputKind.EXTERNAL,):
        return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP,reason=ControlledReadonlyReason.EXTERNAL_SOURCE_REJECTED,adapter_kind=adapter_kind,input_kind=input_kind)
    if input_kind == ControlledInputKind.GITHUB_METADATA:
        return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP,reason=ControlledReadonlyReason.GITHUB_REJECTED,adapter_kind=adapter_kind,input_kind=input_kind)
    return ControlledReadonlyDecision(mode=ControlledReadonlyMode.CANARY_PLAN_ONLY,reason=ControlledReadonlyReason.DISABLED_DEFAULT,adapter_kind=adapter_kind,input_kind=input_kind)

def deny_controlled_readonly_execution(reason:str="denied"): return ControlledReadonlyDecision(mode=ControlledReadonlyMode.DENY_NOOP)
def describe_controlled_readonly_state(cfg): return {"controlled_readonly":"DISABLED","report_reading":"PLAN_ONLY","document_generation":"PLAN_ONLY","local_docs_inspection":"PLAN_ONLY","github_metadata":"DENIED","external_source":"DENIED","zmatrix":"DENIED"}
