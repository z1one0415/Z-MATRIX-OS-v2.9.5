"""Wave0 Triple Gate — three-layer gate evaluation.

Runtime gate → Adapter Framework gate → Individual Adapter gate.
Any gate false / missing / malformed → DENY_DISABLED / NOOP / PLAN_ONLY.
Even if all requested True, enabled decision remains False in P0.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from skillos.capability_invocation_os.adapters.wave0.config import Wave0ExecutionConfig
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


class Wave0GateDecision(Enum):
    DENY_DISABLED = "DENY_DISABLED"
    NOOP = "NOOP"
    PLAN_ONLY = "PLAN_ONLY"


class Wave0GateState(Enum):
    MISSING = "MISSING"
    MALFORMED = "MALFORMED"
    DISABLED = "DISABLED"
    REQUESTED = "REQUESTED"
    # note: there is no ENABLED state in P0


@dataclass(frozen=True)
class Wave0TripleGateDecision:
    runtime_gate: Wave0GateState = Wave0GateState.DISABLED
    adapter_framework_gate: Wave0GateState = Wave0GateState.DISABLED
    individual_adapter_gate: Wave0GateState = Wave0GateState.DISABLED
    final: Wave0GateDecision = Wave0GateDecision.DENY_DISABLED
    reason: str = "P0 disabled-default"


def _evaluate_single_gate(requested: bool) -> Wave0GateState:
    """A single gate evaluates to DISABLED in P0.
    REQUESTED state is recorded only if strict True bool requested.
    There is no ENABLED path."""
    if requested is True:
        return Wave0GateState.REQUESTED
    return Wave0GateState.DISABLED


def evaluate_wave0_triple_gate(
    cfg: Wave0ExecutionConfig,
    adapter_kind: Wave0AdapterKind,
) -> Wave0TripleGateDecision:
    """Evaluate the three-layer gate. P0: final is always DENY_DISABLED."""

    # Gate 1: Runtime gate
    runtime_state = _evaluate_single_gate(cfg.wave0_runtime_requested)

    # Gate 2: Adapter framework gate
    framework_state = _evaluate_single_gate(cfg.wave0_adapter_framework_requested)

    # Gate 3: Individual adapter gate
    adapter_requested_map = {
        Wave0AdapterKind.GITHUB_READONLY: cfg.wave0_github_readonly_requested,
        Wave0AdapterKind.DOCUMENT_GENERATION: cfg.wave0_document_generation_requested,
        Wave0AdapterKind.LOCAL_DOCS: cfg.wave0_local_docs_inspection_requested,
        Wave0AdapterKind.REPORT_READING: cfg.wave0_report_reading_requested,
    }
    adapter_requested = adapter_requested_map.get(adapter_kind, False)
    adapter_state = _evaluate_single_gate(adapter_requested)

    # Determine final: any gate missing/malformed/disabled → DENY
    all_requested = (
        runtime_state == Wave0GateState.REQUESTED
        and framework_state == Wave0GateState.REQUESTED
        and adapter_state == Wave0GateState.REQUESTED
    )

    if all_requested:
        # Even if all gates REQUESTED, P0 still returns PLAN_ONLY (not ENABLED)
        final = Wave0GateDecision.PLAN_ONLY
        reason = "all gates requested but execution not enabled in P0"
    else:
        final = Wave0GateDecision.DENY_DISABLED
        gates_status = []
        if runtime_state != Wave0GateState.REQUESTED:
            gates_status.append("runtime")
        if framework_state != Wave0GateState.REQUESTED:
            gates_status.append("adapter_framework")
        if adapter_state != Wave0GateState.REQUESTED:
            gates_status.append(f"individual_adapter({adapter_kind.name})")
        reason = f"gates not all requested: {', '.join(gates_status)}"

    return Wave0TripleGateDecision(
        runtime_gate=runtime_state,
        adapter_framework_gate=framework_state,
        individual_adapter_gate=adapter_state,
        final=final,
        reason=reason,
    )

# ── Controlled Read-Only Gate ──────────────────────────────────────
@dataclass(frozen=True)
class ControlledReadonlyGateDecision:
    runtime_gate: Wave0GateState = Wave0GateState.DISABLED
    adapter_framework_gate: Wave0GateState = Wave0GateState.DISABLED
    wave0_p0_gate: Wave0GateState = Wave0GateState.DISABLED
    controlled_readonly_gate: Wave0GateState = Wave0GateState.DISABLED
    individual_adapter_gate: Wave0GateState = Wave0GateState.DISABLED
    permission_gate: Wave0GateState = Wave0GateState.DISABLED
    evidence_gate: Wave0GateState = Wave0GateState.DISABLED
    final: str = "DENY_DISABLED"
    reason: str = "P0 disabled-default"

def evaluate_controlled_readonly_gate(cfg, adapter_kind, input_kind) -> ControlledReadonlyGateDecision:
    return ControlledReadonlyGateDecision(reason="P0: all gates disabled, controlled execution not enabled")

class ControlledReadonlyGateState(Enum):
    MISSING = "MISSING"
    MALFORMED = "MALFORMED"
    DISABLED = "DISABLED"
    REQUESTED = "REQUESTED"

