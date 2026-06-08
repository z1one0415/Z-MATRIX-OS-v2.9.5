from skillos.capability_invocation_os.adapters.wave0.permissions import check_permission
from skillos.capability_invocation_os.adapters.wave0.models import Wave0Permission
class TestPerms:
    def test_deny(self): assert check_permission(Wave0Permission.DENY) is False
    def test_read_only(self): assert check_permission(Wave0Permission.READ_ONLY) is False
