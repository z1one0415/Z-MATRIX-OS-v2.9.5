from skillos.capability_invocation_os.runtime.composition import validate_chain
from skillos.capability_invocation_os.runtime.models import InvocationRequest
class TestCompositionNoExecution:
    def test_empty_denied(self): assert validate_chain([]).action == "DENY"
    def test_single_denied(self): assert validate_chain([InvocationRequest()]).action == "DENY"
    def test_multi_denied(self): assert validate_chain([InvocationRequest(), InvocationRequest()]).action == "DENY"
