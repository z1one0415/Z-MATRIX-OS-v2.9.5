"""AdapterRegistry — disabled by default, no dynamic import, no callable storage."""
from skillos.capability_invocation_os.adapters.models import AdapterDescriptor, AdapterId
class AdapterRegistry:
    def __init__(self): self._descriptors = {}; self._registration_enabled = False
    def register_descriptor(self, descriptor):
        if not self._registration_enabled: return None
        self._descriptors[(descriptor.adapter_id.namespace, descriptor.adapter_id.adapter_name)] = descriptor
        return descriptor
    def lookup(self, adapter_id): return self._descriptors.get((adapter_id.namespace, adapter_id.adapter_name))
    def list_descriptors(self): return list(self._descriptors.values())
    def validate_descriptor(self, descriptor): return True
registry = AdapterRegistry()
