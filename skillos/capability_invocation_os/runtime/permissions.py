"""Permission enforcement — T5 never granted, T3/T4 require human token."""
from skillos.capability_invocation_os.runtime.models import RiskTier
def check_permission(requested_tier, caller_role="", has_human_token=False):
    if requested_tier == RiskTier.T5: return False
    if requested_tier in (RiskTier.T3, RiskTier.T4): return has_human_token
    return False
def require_human_token_for_tier(tier): return tier in (RiskTier.T3, RiskTier.T4)
