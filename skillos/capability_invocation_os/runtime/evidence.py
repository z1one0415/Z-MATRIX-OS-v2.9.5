"""Evidence sinks — NoopSink default, InMemorySink optional, no file/network."""
from skillos.capability_invocation_os.runtime.models import EvidenceRecord
from skillos.capability_invocation_os.runtime.hashlock import stable_hash_dict
class NoopEvidenceSink:
    def record(self, evidence): pass
    def flush(self): pass
class InMemoryEvidenceSink:
    def __init__(self): self.records = []
    def record(self, evidence): self.records.append(evidence)
    def flush(self): self.records.clear()
def compute_pre_hash(data): return stable_hash_dict(data) if data else ""
def compute_post_hash(data): return stable_hash_dict(data) if data else ""
