"""Wave0 Enablement Control — plan/request/deny/describe.

No execute. No run. No call. No invoke.
No real adapter action.
Returns internal decision objects only.
Decision result: DISABLED / DENY_NOOP / PLAN_ONLY.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.gates import (
    Wave0GateDecision,
    Wave0GateState,
    Wave0TripleGateDecision,
    evaluate_wave0_triple_gate,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


class EnablementAction(Enum):
    DISABLED = "DISABLED"
    DENY_NOOP = "DENY_NOOP"
    PLAN_ONLY = "PLAN_ONLY"


@dataclass(frozen=True)
class EnablementDecision:
    action: EnablementAction
    reason: str
    adapter_kind: Optional[Wave0AdapterKind] = None
    gate_decision: Optional[Wave0TripleGateDecision] = None


def request_controlled_readonly(cfg, adapter_kind, input_kind):
    return EnablementDecision(action=EnablementAction.DISABLED, reason="P0: controlled readonly execution disabled")


def deny_controlled_readonly(reason: str = "disabled"):
    return EnablementDecision(action=EnablementAction.DENY_NOOP, reason=reason)


def plan_controlled_readonly(cfg, adapter_kind, input_kind):
    return EnablementDecision(action=EnablementAction.PLAN_ONLY, reason="P0: planning only, no execution")


def plan_wave0_enablement(
    cfg: Wave0ExecutionConfig,
    adapter_kind: Wave0AdapterKind,
) -> EnablementDecision:
    """Plan enablement steps. No execution. Returns PLAN_ONLY if all gates requested."""
    gate = evaluate_wave0_triple_gate(cfg, adapter_kind)
    if gate.final == Wave0GateDecision.PLAN_ONLY:
        return EnablementDecision(
            action=EnablementAction.PLAN_ONLY,
            reason="all gates requested, planning allowed, execution not enabled",
            adapter_kind=adapter_kind,
            gate_decision=gate,
        )
    return EnablementDecision(
        action=EnablementAction.DENY_NOOP,
        reason=f"planning denied: {gate.reason}",
        adapter_kind=adapter_kind,
        gate_decision=gate,
    )


def request_wave0_enablement(
    cfg: Wave0ExecutionConfig,
    adapter_kind: Wave0AdapterKind,
) -> EnablementDecision:
    """Request enablement. Records intent. Does not enable."""
    gate = evaluate_wave0_triple_gate(cfg, adapter_kind)
    return EnablementDecision(
        action=EnablementAction.DISABLED,
        reason=f"request recorded but execution disabled in P0: {gate.reason}",
        adapter_kind=adapter_kind,
        gate_decision=gate,
    )


def deny_wave0_execution(reason: str) -> EnablementDecision:
    """Explicit denial. No execution."""
    return EnablementDecision(action=EnablementAction.DENY_NOOP, reason=reason)


def describe_enablement_state(
    cfg: Wave0ExecutionConfig,
) -> Dict[str, str]:
    """Return human-readable enablement state. All disabled in P0."""
    adapters = {
        "wave0_runtime": cfg.wave0_runtime_requested,
        "adapter_framework": cfg.wave0_adapter_framework_requested,
        "github_readonly": cfg.wave0_github_readonly_requested,
        "document_generation": cfg.wave0_document_generation_requested,
        "local_docs_inspection": cfg.wave0_local_docs_inspection_requested,
        "report_reading": cfg.wave0_report_reading_requested,
    }
    return {
        name: "REQUESTED (not enabled — P0 disabled-default)" if requested else "DISABLED"
        for name, requested in adapters.items()
    }

# ── Controlled Read-Only ──────────────────────────────────
def request_controlled_readonly(cfg, adapter_kind, input_kind):
    from .enablement import EnablementDecision, EnablementAction
    return EnablementDecision(action=EnablementAction.DISABLED, reason="P0: disabled")

def deny_controlled_readonly(reason: str = "disabled"):
    from .enablement import EnablementDecision, EnablementAction
    return EnablementDecision(action=EnablementAction.DENY_NOOP, reason=reason)

def plan_controlled_readonly(cfg, adapter_kind, input_kind):
    from .enablement import EnablementDecision, EnablementAction
    return EnablementDecision(action=EnablementAction.PLAN_ONLY, reason="P0: planning only")
