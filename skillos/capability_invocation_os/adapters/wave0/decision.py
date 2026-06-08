"""Wave0 Enablement Decision Model — internal-only.

No caller-visible warning fields.
No result_envelope mutation fields.
No execute/call/run/invoke fields.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Wave0EnablementReason(Enum):
    DISABLED_DEFAULT = "P0 disabled-default"
    GATE_NOT_REQUESTED = "gate not fully requested"
    KILL_SWITCH_ACTIVE = "kill switch override"
    PERMISSION_DENIED = "permission check failed"
    PLAN_ONLY = "planning only, execution not allowed"


@dataclass(frozen=True)
class Wave0EnablementBoundary:
    """Boundary enforcement — all must be True for any future enablement."""
    no_runtime_enablement: bool = True
    no_adapter_execution: bool = True
    no_capability_execution: bool = True
    no_real_adapter_call: bool = True
    no_network_call: bool = True
    no_file_read_write: bool = True
    no_zmatrix_import: bool = True
    no_warning_enablement: bool = True
    no_result_envelope_mutation: bool = True
    no_blocking: bool = True
    no_fail_closed: bool = True
    no_production: bool = True
    level5_blocked: bool = True


@dataclass(frozen=True)
class Wave0EnablementProofHint:
    """Hints for proof harness verification."""
    disabled_default_proofs: List[str] = field(default_factory=lambda: [
        "all_enabled_return_false",
        "requested_does_not_enable",
        "non_bool_truthy_disabled",
        "env_cannot_enable",
        "malformed_config_disabled",
        "missing_config_disabled",
    ])
    triple_gate_proofs: List[str] = field(default_factory=lambda: [
        "any_gate_missing_disabled",
        "any_gate_malformed_disabled",
        "all_requested_still_plan_only",
    ])
    kill_switch_proofs: List[str] = field(default_factory=lambda: [
        "master_kill_overrides_all",
        "per_adapter_kill_overrides_gate",
        "evidence_kill_blocks_sink",
        "output_kill_blocks_generation",
    ])
    permission_proofs: List[str] = field(default_factory=lambda: [
        "write_denied",
        "production_denied",
        "broker_denied",
        "real_trade_denied",
        "network_denied",
        "file_write_denied",
        "unknown_permission_denied",
    ])


@dataclass(frozen=True)
class Wave0EnablementDecision:
    """Internal-only enablement decision. Not exposed to caller."""
    allowed: bool = False  # P0: always False
    reason: Wave0EnablementReason = Wave0EnablementReason.DISABLED_DEFAULT
    boundary: Wave0EnablementBoundary = field(default_factory=Wave0EnablementBoundary)
    proofs: Wave0EnablementProofHint = field(default_factory=Wave0EnablementProofHint)
    gate_state: Optional[str] = None
    kill_state: Optional[str] = None
    perm_state: Optional[str] = None
