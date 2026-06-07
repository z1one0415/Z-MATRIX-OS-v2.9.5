from skillos.capability_invocation_os.runtime.contracts import validate
from skillos.capability_invocation_os.runtime.models import InvocationRequest, CapabilityContract, RiskTier, PermissionTier
class TestContractsNoExecution:
    def test_validate_denies(self):
        r = validate(InvocationRequest(), CapabilityContract())
        assert r.action == "DENY"
