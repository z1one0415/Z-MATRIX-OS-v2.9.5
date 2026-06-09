import pytest
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.permissions import (
    A1_T0_DOCS_ONLY,
    A1_T1_BRIDGE_REGISTRY_READONLY,
    A1_T2_BRIDGE_EVIDENCE_READONLY,
    A1_T3_BRIDGE_CONTEXT_DRY_PLAN,
    ALLOWED_TIERS,
    is_bridge_permission_allowed,
    resolve_bridge_permission_tier,
    deny_bridge_permission,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeDecision,
)


def test_readonly_bridge_tiers_defined():
    assert A1_T0_DOCS_ONLY == "A1_T0_DOCS_ONLY"
    assert A1_T1_BRIDGE_REGISTRY_READONLY == "A1_T1_BRIDGE_REGISTRY_READONLY"
    assert A1_T2_BRIDGE_EVIDENCE_READONLY == "A1_T2_BRIDGE_EVIDENCE_READONLY"
    assert A1_T3_BRIDGE_CONTEXT_DRY_PLAN == "A1_T3_BRIDGE_CONTEXT_DRY_PLAN"


def test_execution_write_production_broker_real_trade_denied():
    assert is_bridge_permission_allowed(A1_T0_DOCS_ONLY) is True
    assert is_bridge_permission_allowed(A1_T1_BRIDGE_REGISTRY_READONLY) is True
    assert is_bridge_permission_allowed(A1_T2_BRIDGE_EVIDENCE_READONLY) is True
    assert is_bridge_permission_allowed(A1_T3_BRIDGE_CONTEXT_DRY_PLAN) is True

    for forbidden in ["EXECUTION", "WRITE", "PRODUCTION", "BROKER", "REAL_TRADE", "Z8_RUNTIME", "V3_SANDBOX"]:
        assert is_bridge_permission_allowed(forbidden) is False


def test_no_execution_tier_in_allowed():
    assert "EXECUTION" not in ALLOWED_TIERS
    assert "WRITE" not in ALLOWED_TIERS
    assert "PRODUCTION" not in ALLOWED_TIERS
    assert "BROKER" not in ALLOWED_TIERS
    assert "REAL_TRADE" not in ALLOWED_TIERS

    result = resolve_bridge_permission_tier("any", "any")
    assert result == A1_T0_DOCS_ONLY

    denied = deny_bridge_permission("execution denied")
    assert denied == A1FactorBridgeDecision.DENY_BRIDGE_EXECUTION_FORBIDDEN
