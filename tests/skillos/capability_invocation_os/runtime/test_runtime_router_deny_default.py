from skillos.capability_invocation_os.runtime.router import route
from skillos.capability_invocation_os.runtime.models import InvocationRequest
class TestRouterDenyDefault:
    def test_denies(self): assert route(InvocationRequest()).action == "DENY"
