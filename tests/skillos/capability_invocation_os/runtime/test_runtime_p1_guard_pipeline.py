from skillos.capability_invocation_os.runtime.guard import run_guard_pipeline
from skillos.capability_invocation_os.runtime.models import InvocationRequest
from skillos.capability_invocation_os.runtime.config import load_config
class TestP1GuardPipeline:
    def test_disabled_continues(self):
        c=load_config(None); r=run_guard_pipeline(InvocationRequest(),config=c)
        assert r.action == "CONTINUE"; assert r.degraded is True
    def test_ten_stages(self):
        r=run_guard_pipeline(InvocationRequest())
        assert len(r.stage_results) == 10
    def test_not_blocked(self):
        assert run_guard_pipeline(InvocationRequest()).action != "BLOCKED"
    def test_not_fail_closed(self):
        assert run_guard_pipeline(InvocationRequest()).action != "FAIL_CLOSED"
