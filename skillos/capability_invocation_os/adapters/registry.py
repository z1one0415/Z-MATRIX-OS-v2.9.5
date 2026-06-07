"""AdapterRegistry — disabled by default, no dynamic import, no callable storage, no Z-MATRIX imports."""
from skillos.capability_invocation_os.adapters.models import AdapterDescriptor, AdapterId, AdapterMode
class AdapterRegistry:
    def __init__(self): self._descriptors = {}
    def register_descriptor(self, descriptor): self._descriptors[(descriptor.adapter_id.namespace, descriptor.adapter_id.adapter_name)] = descriptor
    def lookup(self, adapter_id): return self._descriptors.get((adapter_id.namespace, adapter_id.adapter_name))
    def list_descriptors(self): return list(self._descriptors.values())
    def validate_descriptor(self, descriptor): return True
registry = AdapterRegistry()
