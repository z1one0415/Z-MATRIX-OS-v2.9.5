from skillos.capability_invocation_os.runtime.permissions import check_permission, require_human_token_for_tier
from skillos.capability_invocation_os.runtime.models import RiskTier
class TestP1PermissionEnforcement:
    def test_t5_denied(self): assert check_permission(RiskTier.T5,"admin",True) is False
    def test_t3_needs_token(self): assert check_permission(RiskTier.T3,"admin",False) is False
    def test_t3_with_token(self): assert check_permission(RiskTier.T3,"admin",True) is True
    def test_require_human(self): assert require_human_token_for_tier(RiskTier.T3) is True
    def test_t1_denied_default(self): assert check_permission(RiskTier.T1,"anyone") is False
