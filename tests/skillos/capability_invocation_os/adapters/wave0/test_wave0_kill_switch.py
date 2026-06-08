from skillos.capability_invocation_os.adapters.wave0.kill_switch import ks, get_kill_switch
class TestKS:
    def test_master(self):
        k = ks()
        assert k.master is True
    def test_github(self):
        k = ks()
        assert k.github is True
    def test_disable_all(self):
        k = ks()
        k.disable_all()
        assert k.master is True
