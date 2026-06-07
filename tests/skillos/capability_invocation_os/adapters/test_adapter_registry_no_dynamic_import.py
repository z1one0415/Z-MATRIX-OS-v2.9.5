from skillos.capability_invocation_os.adapters.registry import registry
from skillos.capability_invocation_os.adapters.models import AdapterId
class TestAdapterRegistryNoDynamicImport:
    def test_empty_lookup(self): assert registry.lookup(AdapterId(namespace="test",adapter_name="x")) is None
    def test_empty_list(self): assert registry.list_descriptors() == []
