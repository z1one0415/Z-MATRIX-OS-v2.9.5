"""Adapter evidence sinks — Noop by default, no file/network, no Z-MATRIX imports."""
from skillos.capability_invocation_os.adapters.models import AdapterEvidenceSpec
class NoopAdapterEvidenceSink:
    def record(self,evidence): pass
    def flush(self): pass
class InMemoryAdapterEvidenceSink:
    def __init__(self): self.records = []
    def record(self,evidence): self.records.append(evidence)
    def flush(self): self.records.clear()
