from skillos.capability_invocation_os.runtime.contracts import validate_contract, validate_forbidden_actions
from skillos.capability_invocation_os.runtime.models import InvocationRequest, CapabilityContract
class TestP1ContractValidation:
    def test_validate_needs_review(self):
        r=validate_contract(InvocationRequest(), CapabilityContract())
        assert r.action in ("DENY_NOOP","NEEDS_HUMAN_REVIEW")
    def test_forbidden_actions_checked(self):
        c=CapabilityContract(forbidden_actions=["execution_capability"])
        r=validate_forbidden_actions(c); assert r.action == "DENY"
