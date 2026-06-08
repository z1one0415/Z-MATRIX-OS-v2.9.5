import pytest
from skillos.capability_invocation_os.adapters.factor_library.permissions import (
    is_permission_allowed, resolve_permission_tier, T1_REGISTRY_READONLY,
    EXECUTION_DENIED,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import CANONICAL_READONLY_INTENTS

def test_readonly_tiers_exist():
    assert T1_REGISTRY_READONLY == "T1"

def test_all_permissions_denied():
    for intent in CANONICAL_READONLY_INTENTS:
        assert is_permission_allowed("T0", intent) is False

def test_resolve_tier():
    assert resolve_permission_tier("REGISTRY_READ") == T1_REGISTRY_READONLY
    assert resolve_permission_tier("ALPHA_SIGNAL") == EXECUTION_DENIED
