from skillos.capability_invocation_os.adapters.kill_switch import kill_switch
class TestAdapterKillSwitch:
    def test_master_disabled(self): assert kill_switch.master_disable is True
    def test_execution_disabled(self): assert kill_switch.execution_disable is True
    def test_module_disabled(self): assert kill_switch.module_adapter_disable is True
    def test_disable_all(self): kill_switch.disable_all(); assert kill_switch.master_disable is True
