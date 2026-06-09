A1_T0_DOCS_ONLY = "A1_T0_DOCS_ONLY"
A1_T1_BRIDGE_REGISTRY_READONLY = "A1_T1_BRIDGE_REGISTRY_READONLY"
A1_T2_BRIDGE_EVIDENCE_READONLY = "A1_T2_BRIDGE_EVIDENCE_READONLY"
A1_T3_BRIDGE_CONTEXT_DRY_PLAN = "A1_T3_BRIDGE_CONTEXT_DRY_PLAN"

FORBIDDEN_TIERS = frozenset({
    "EXECUTION", "WRITE", "PRODUCTION", "BROKER",
    "REAL_TRADE", "Z8_RUNTIME", "V3_SANDBOX",
})

ALLOWED_TIERS = frozenset({
    A1_T0_DOCS_ONLY,
    A1_T1_BRIDGE_REGISTRY_READONLY,
    A1_T2_BRIDGE_EVIDENCE_READONLY,
    A1_T3_BRIDGE_CONTEXT_DRY_PLAN,
})

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeDecision,
)


def resolve_bridge_permission_tier(source_class: str, intent: str) -> str:
    return A1_T0_DOCS_ONLY


def is_bridge_permission_allowed(tier: str) -> bool:
    if tier in ALLOWED_TIERS:
        return True
    if tier.upper() in FORBIDDEN_TIERS:
        return False
    if any(kw in tier.upper() for kw in FORBIDDEN_TIERS):
        return False
    return False


def deny_bridge_permission(reason: str) -> A1FactorBridgeDecision:
    return A1FactorBridgeDecision.DENY_BRIDGE_EXECUTION_FORBIDDEN
