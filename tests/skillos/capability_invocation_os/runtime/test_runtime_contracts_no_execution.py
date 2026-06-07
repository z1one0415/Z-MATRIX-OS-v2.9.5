import pytest
from skillos.capability_invocation_os.runtime.contracts import validate_contract
from skillos.capability_invocation_os.runtime.models import InvocationRequest, CapabilityContract
class TestContractsNoExecution:
    def test_validate_denies(self):
        r = validate_contract(InvocationRequest(), CapabilityContract())
        assert r.action in ("DENY_NOOP", "NEEDS_HUMAN_REVIEW")
