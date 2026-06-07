"""NoopEvidenceSink — no file writes, no stdout/stderr."""
class NoopEvidenceSink:
    def record(self, evidence) -> None: pass
    def flush(self) -> None: pass
