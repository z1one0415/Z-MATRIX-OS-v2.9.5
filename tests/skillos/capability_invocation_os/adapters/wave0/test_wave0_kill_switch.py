from skillos.capability_invocation_os.adapters.wave0.kill_switch import ks
class TestKS:
    def test_master(self): assert ks.master is True
    def test_github(self): assert ks.github is True
    def test_disable_all(self): ks.disable_all(); assert ks.master is True
