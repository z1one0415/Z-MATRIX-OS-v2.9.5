"""Adapter permissions — T5/REAL_TRADE/BROKER always denied, no enablement, no Z-MATRIX imports."""
from skillos.capability_invocation_os.adapters.models import AdapterPermissionTier
def check_permission(requested, has_human_token=False):
    if requested in (AdapterPermissionTier.NEVER_REAL_TRADE, AdapterPermissionTier.NO_PRODUCTION, AdapterPermissionTier.DENY): return False
    if requested in (AdapterPermissionTier.ADVISORY,): return has_human_token
    return False
