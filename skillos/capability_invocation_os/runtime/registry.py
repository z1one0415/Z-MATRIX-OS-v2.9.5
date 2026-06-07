"""Static registry — deny unknown, no dynamic import, no adapter load."""
from skillos.capability_invocation_os.runtime.models import CapabilityId, CapabilityContract, RiskTier, PermissionTier

_REGISTRY = {}

def lookup(cap_id: CapabilityId):
    if not _REGISTRY:
        return CapabilityContract(risk_tier=RiskTier.T5, permission_required=PermissionTier.BLOCKED, human_approval_required=True)
    return _REGISTRY.get((cap_id.module, cap_id.capability_name), CapabilityContract(risk_tier=RiskTier.T5, permission_required=PermissionTier.BLOCKED))

def is_capability_known(cap_id: CapabilityId) -> bool:
    return (cap_id.module, cap_id.capability_name) in _REGISTRY
