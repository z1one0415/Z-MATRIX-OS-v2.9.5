from skillos.capability_invocation_os.adapters.base import AdapterBase
class TestAdapterBaseNoExecution:
    def test_no_execute(self): assert not hasattr(AdapterBase(),"execute")
    def test_no_run(self): assert not hasattr(AdapterBase(),"run")
    def test_no_call(self): assert not hasattr(AdapterBase(),"call")
    def test_no_invoke(self): assert not hasattr(AdapterBase(),"invoke")
    def test_deny_works(self): assert AdapterBase().deny().action == "DENY"
    def test_describe_works(self): assert AdapterBase().describe() is not None
