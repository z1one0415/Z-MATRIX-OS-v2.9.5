from skillos.capability_invocation_os.runtime.kill_switch import kill_switch
class TestP1KillSwitch:
    def test_all_disabled(self):
        assert kill_switch.master_disable is True
        assert kill_switch.registry_disable is True
        assert kill_switch.capability_execution_disable is True
    def test_disable_all(self):
        kill_switch.disable_all()
        assert kill_switch.master_disable is True
