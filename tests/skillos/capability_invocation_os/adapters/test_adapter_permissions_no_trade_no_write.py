from skillos.capability_invocation_os.adapters.permissions import check_permission
from skillos.capability_invocation_os.adapters.models import AdapterPermissionTier
class TestAdapterPermissions:
    def test_never_real_trade(self): assert check_permission(AdapterPermissionTier.NEVER_REAL_TRADE) is False
    def test_deny(self): assert check_permission(AdapterPermissionTier.DENY) is False
    def test_read_only_denied(self): assert check_permission(AdapterPermissionTier.READ_ONLY) is False
