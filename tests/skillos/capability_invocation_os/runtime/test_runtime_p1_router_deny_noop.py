from skillos.capability_invocation_os.runtime.router import route, classify_request, select_candidate_capabilities
from skillos.capability_invocation_os.runtime.models import InvocationRequest
from skillos.capability_invocation_os.runtime.config import load_config
class TestP1RouterDenyNoop:
    def test_disabled_denies(self):
        c=load_config(None); r=route(InvocationRequest(),config=c)
        assert r.action == "DENY_NOOP"
    def test_classify_unknown(self):
        r=classify_request(InvocationRequest()); assert r["action"] == "DENY"
    def test_no_candidates(self):
        assert select_candidate_capabilities(InvocationRequest()) == []
