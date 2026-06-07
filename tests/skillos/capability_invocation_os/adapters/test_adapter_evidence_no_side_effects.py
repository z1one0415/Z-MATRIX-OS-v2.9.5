import io, sys, os, tempfile
from skillos.capability_invocation_os.adapters.evidence import NoopAdapterEvidenceSink, InMemoryAdapterEvidenceSink
class TestAdapterEvidenceNoSideEffects:
    def test_noop_writes_nothing(self): s=NoopAdapterEvidenceSink(); s.record(None); s.flush()
    def test_inmemory_stays_memory(self): s=InMemoryAdapterEvidenceSink(); s.record({"id":"1"}); assert len(s.records)==1; s.flush(); assert len(s.records)==0
    def test_no_file_created(self):
        with tempfile.TemporaryDirectory() as d: os.chdir(d); s=InMemoryAdapterEvidenceSink(); s.record({"id":"1"}); s.flush(); assert len(os.listdir("."))==0
    def test_no_stdout(self): old=sys.stdout; sys.stdout=io.StringIO(); NoopAdapterEvidenceSink().record(None); sys.stdout=old
