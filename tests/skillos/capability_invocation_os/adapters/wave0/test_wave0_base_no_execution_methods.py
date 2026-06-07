from skillos.capability_invocation_os.adapters.wave0.base import Wave0AdapterSkeleton
class TestBase:
    def test_no_execute(self): assert not hasattr(Wave0AdapterSkeleton(),"execute")
    def test_no_run(self): assert not hasattr(Wave0AdapterSkeleton(),"run")
    def test_no_call(self): assert not hasattr(Wave0AdapterSkeleton(),"call")
    def test_no_invoke(self): assert not hasattr(Wave0AdapterSkeleton(),"invoke")
    def test_deny(self): assert Wave0AdapterSkeleton().deny().action=="DENY"
