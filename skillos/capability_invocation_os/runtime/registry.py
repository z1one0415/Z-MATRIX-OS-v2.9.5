"""Static registry — deny unknown, no dynamic import, no callable storage."""
from skillos.capability_invocation_os.runtime.models import CapabilityId, CapabilityContract, RiskTier, PermissionTier
from skillos.capability_invocation_os.runtime.validation import validate_no_forbidden_modules

class StaticRegistry:
    def __init__(self): self._entries = {}
    def load(self, entries=None):
        self._entries.clear()
        if entries:
            for e in entries:
                v = validate_no_forbidden_modules([e.get("module","")])
                if v.valid: self._entries[(e["module"], e["capability_name"])] = CapabilityContract(skill_id=e.get("skill_id",""), risk_tier=RiskTier(int(e.get("risk_tier","5"))), permission_required=PermissionTier(int(e.get("permission","6"))))
    def lookup(self, cap_id):
        if not self._entries: return CapabilityContract(risk_tier=RiskTier.T5, permission_required=PermissionTier.BLOCKED)
        return self._entries.get((cap_id.module, cap_id.capability_name), CapabilityContract(risk_tier=RiskTier.T5, permission_required=PermissionTier.BLOCKED))
    def is_known(self, cap_id): return (cap_id.module, cap_id.capability_name) in self._entries
    def validate_entry(self, entry):
        return validate_no_forbidden_modules([entry.get("module","")])

registry = StaticRegistry()
