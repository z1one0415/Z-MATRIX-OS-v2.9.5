"""Wave0 evidence sinks — Noop default, InMemory optional, no file/network."""
class NoopWave0EvidenceSink:
    def record(self,e): pass
    def flush(self): pass
class InMemoryWave0EvidenceSink:
    def __init__(self): self.records=[]
    def record(self,e): self.records.append(e)
    def flush(self): self.records.clear()
