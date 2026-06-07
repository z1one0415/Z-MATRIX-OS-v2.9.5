import io, sys, os, tempfile
from skillos.capability_invocation_os.runtime.evidence import NoopEvidenceSink, InMemoryEvidenceSink, compute_pre_hash
class TestP1EvidenceInMemoryOnly:
    def test_noop_writes_nothing(self):
        s=NoopEvidenceSink(); s.record(None); s.flush()
    def test_inmemory_stays_in_memory(self):
        s=InMemoryEvidenceSink(); s.record({"id":"1"}); assert len(s.records)==1; s.flush(); assert len(s.records)==0
    def test_no_file_created(self):
        with tempfile.TemporaryDirectory() as d: os.chdir(d)
        s=InMemoryEvidenceSink(); s.record({"id":"1"}); s.flush()
        assert len(os.listdir("."))==0
    def test_pre_hash(self):
        assert compute_pre_hash({"a":1}) == compute_pre_hash({"a":1})
    def test_no_stdout(self):
        old=sys.stdout; sys.stdout=io.StringIO()
        try: NoopEvidenceSink().record(None)
        finally: sys.stdout=old
