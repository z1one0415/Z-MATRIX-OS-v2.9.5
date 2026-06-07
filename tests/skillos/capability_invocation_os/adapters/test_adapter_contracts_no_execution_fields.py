from skillos.capability_invocation_os.adapters.contracts import validate_adapter_contract, validate_adapter_request, validate_forbidden_actions
from skillos.capability_invocation_os.adapters.models import AdapterContract, AdapterRequest
class TestAdapterContractsNoExecution:
    def test_validate_contract(self): assert validate_adapter_contract(AdapterContract()).valid is True
    def test_request_denied(self): assert validate_adapter_request(AdapterRequest(), AdapterContract()).action == "DENY"
    def test_forbidden_detected(self): assert validate_forbidden_actions(AdapterContract(forbidden_actions=["real_trade"])).action == "DENY"
