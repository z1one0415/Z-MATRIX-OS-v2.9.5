from skillos.capability_invocation_os.runtime.guard import run_guard_pipeline
from skillos.capability_invocation_os.runtime.models import InvocationRequest
class TestGuardNoBlocking:
    def test_continues(self):
        r = run_guard_pipeline(InvocationRequest())
        assert r.action == "CONTINUE"
        assert r.degraded is True
    def test_action_not_blocked(self):
        assert run_guard_pipeline(InvocationRequest()).action != "BLOCKED"
