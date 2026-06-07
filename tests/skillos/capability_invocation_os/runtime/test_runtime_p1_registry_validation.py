from skillos.capability_invocation_os.runtime.registry import StaticRegistry
from skillos.capability_invocation_os.runtime.models import CapabilityId, RiskTier
class TestP1RegistryValidation:
    def test_empty_denies(self):
        r=StaticRegistry(); c=r.lookup(CapabilityId(module="test",capability_name="x"))
        assert c.risk_tier == RiskTier.T5
    def test_unknown_denies(self):
        r=StaticRegistry(); r.load([{"module":"allowed","capability_name":"read","skill_id":"1","risk_tier":1,"permission":1}])
        c=r.lookup(CapabilityId(module="unknown",capability_name="x"))
        assert c.risk_tier == RiskTier.T5
    def test_known_found(self):
        r=StaticRegistry(); r.load([{"module":"mod","capability_name":"cap","skill_id":"1","risk_tier":1,"permission":1}])
        c=r.lookup(CapabilityId(module="mod",capability_name="cap"))
        assert c.risk_tier == RiskTier.T1
    def test_forbidden_module_rejected(self):
        r=StaticRegistry(); entry={"module":"z2","capability_name":"research"}
        v=r.validate_entry(entry); assert v.valid is False