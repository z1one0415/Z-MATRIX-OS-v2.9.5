from skillos.capability_invocation_os.runtime.registry import lookup, is_capability_known
from skillos.capability_invocation_os.runtime.models import CapabilityId, RiskTier
class TestRegistryNoExecution:
    def test_unknown_returns_t5(self):
        c = lookup(CapabilityId(module="nonexistent", capability_name="test"))
        assert c.risk_tier == RiskTier.T5
    def test_unknown_not_known(self):
        assert is_capability_known(CapabilityId(module="z2", capability_name="research")) is False
