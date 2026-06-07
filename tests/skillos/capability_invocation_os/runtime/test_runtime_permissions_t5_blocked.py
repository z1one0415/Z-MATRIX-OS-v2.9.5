from skillos.capability_invocation_os.runtime.permissions import check_permission
from skillos.capability_invocation_os.runtime.models import RiskTier
class TestPermissionsT5Blocked:
    def test_t5_never_granted(self): assert check_permission(RiskTier.T5, "admin", True) is False
    def test_t3_denied_without_token(self): assert check_permission(RiskTier.T3, "admin", False) is False
    def test_deny_by_default(self): assert check_permission(RiskTier.T1, "anyone") is False
