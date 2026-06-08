import io,sys,os,tempfile
from skillos.capability_invocation_os.adapters.wave0.evidence import NoopWave0EvidenceSink, InMemoryWave0EvidenceSink
class TestEvidence:
    def test_noop(self): s=NoopWave0EvidenceSink(); s.record(None); s.flush()
    def test_memory(self): s=InMemoryWave0EvidenceSink(); s.record({"id":"1"}); assert len(s.records)==1; s.flush(); assert len(s.records)==0
    def test_no_file(self):
        with tempfile.TemporaryDirectory() as d: os.chdir(d); s=InMemoryWave0EvidenceSink(); s.record({"id":"1"}); s.flush(); assert len(os.listdir("."))==0
