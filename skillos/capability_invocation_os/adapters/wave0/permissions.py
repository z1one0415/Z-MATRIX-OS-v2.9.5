"""Wave0 Permissions — all denied by default.

- unknown → denied
- write → denied
- production → denied
- broker → denied
- real_trade → denied
- network → denied (unless future explicit read gate)
- file_write → denied
- generation-only is non-execution
"""

from enum import Enum
from typing import Optional
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind, Wave0Permission


class Wave0ExecutionPermission(Enum):
    """Permissions for execution enablement layer."""
    READ_ONLY = "READ_ONLY"
    GENERATION_ONLY = "GENERATION_ONLY"
    WRITE = "WRITE"
    PRODUCTION = "PRODUCTION"
    BROKER = "BROKER"
    REAL_TRADE = "REAL_TRADE"
    NETWORK = "NETWORK"
    FILE_WRITE = "FILE_WRITE"
    DENY = "DENY"


# Always-denied permissions (even in future phases)
ALWAYS_DENIED = frozenset({
    Wave0ExecutionPermission.WRITE,
    Wave0ExecutionPermission.PRODUCTION,
    Wave0ExecutionPermission.BROKER,
    Wave0ExecutionPermission.REAL_TRADE,
    Wave0ExecutionPermission.FILE_WRITE,
})


def validate_wave0_execution_permission(
    adapter_kind: Wave0AdapterKind,
    permission: Wave0ExecutionPermission,
) -> bool:
    """Validate execution permission. P0: always returns False (denied).

    Args:
        adapter_kind: The adapter requesting execution
        permission: The permission being requested

    Returns:
        False always in P0 (all execution denied)
    """
    # Always deny forbidden permissions
    if permission in ALWAYS_DENIED:
        return False

    # Unknown permission → denied
    if not isinstance(permission, Wave0ExecutionPermission):
        return False

    # P0: all execution denied
    return False


def check_permission(requested) -> bool:
    """Backward-compatible permission check. P0: always denies."""
    if requested is None:
        return False
    if isinstance(requested, Wave0Permission):
        if requested == Wave0Permission.DENY:
            return False
    return False


def can_read(adapter_kind: Wave0AdapterKind) -> bool:
    """Check if adapter can read. P0: False (no execution)."""
    return False


def can_generate(adapter_kind: Wave0AdapterKind) -> bool:
    """Check if adapter can generate output. P0: False."""
    return False


def validate_controlled_readonly_permission(adapter_kind, input_kind, permission) -> bool: return False
