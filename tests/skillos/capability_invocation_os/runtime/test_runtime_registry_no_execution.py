import pytest
from skillos.capability_invocation_os.runtime.registry import StaticRegistry
from skillos.capability_invocation_os.runtime.models import CapabilityId, RiskTier
class TestRegistryNoExecution:
    def setup_method(self): self.reg = StaticRegistry()
    def test_unknown_returns_t5(self):
        c = self.reg.lookup(CapabilityId(module="nonexistent", capability_name="test"))
        assert c.risk_tier == RiskTier.T5
    def test_unknown_not_known(self):
        assert self.reg.is_known(CapabilityId(module="z2", capability_name="research")) is False
