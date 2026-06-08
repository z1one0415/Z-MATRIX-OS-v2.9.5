"""Permissions — P0: all denied. No execution/write/production tiers."""

T0_DOCS_ONLY = "T0"
T1_REGISTRY_READONLY = "T1"
T2_EVIDENCE_READONLY = "T2"
T3_RESEARCH_CONTEXT_DRY_PLAN = "T3"
EXECUTION_DENIED = "EXECUTION_DENIED"
WRITE_DENIED = "WRITE_DENIED"
PRODUCTION_DENIED = "PRODUCTION_DENIED"
BROKER_DENIED = "BROKER_DENIED"
REAL_TRADE_DENIED = "REAL_TRADE_DENIED"

from skillos.capability_invocation_os.adapters.factor_library.constants import CANONICAL_READONLY_INTENTS
from skillos.capability_invocation_os.adapters.factor_library.models import FactorAdapterDecision, FactorInvocationRequest
from skillos.capability_invocation_os.adapters.factor_library.degradation import disabled_default_noop, deny_execution_forbidden

def is_permission_allowed(tier: str, intent: str) -> bool:
    return False

def resolve_permission_tier(intent: str) -> str:
    if intent in CANONICAL_READONLY_INTENTS:
        return T1_REGISTRY_READONLY
    return EXECUTION_DENIED

def deny_execution_permission(reason: str) -> FactorAdapterDecision:
    return deny_execution_forbidden()
