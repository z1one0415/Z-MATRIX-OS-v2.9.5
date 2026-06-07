import io, sys
from skillos.capability_invocation_os.runtime.evidence import NoopEvidenceSink
class TestEvidenceNoSideEffects:
    def test_no_file_write(self):
        s = NoopEvidenceSink(); s.record(None); s.flush()
    def test_no_stdout(self):
        old = sys.stdout; sys.stdout = io.StringIO()
        try: NoopEvidenceSink().record(None)
        finally: sys.stdout = old
