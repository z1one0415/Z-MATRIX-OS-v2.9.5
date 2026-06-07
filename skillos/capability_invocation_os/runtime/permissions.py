"""Permission enforcement — T5 never granted, deny-by-default."""
from skillos.capability_invocation_os.runtime.models import RiskTier, PermissionTier

def check_permission(requested_tier: RiskTier, caller_role: str, has_human_token: bool = False) -> bool:
    if requested_tier == RiskTier.T5:
        return False
    if requested_tier in (RiskTier.T3, RiskTier.T4):
        return has_human_token
    return False
