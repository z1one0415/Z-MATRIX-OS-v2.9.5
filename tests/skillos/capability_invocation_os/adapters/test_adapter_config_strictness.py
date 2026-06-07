from skillos.capability_invocation_os.adapters.config import load_config, is_adapter_framework_enabled, is_requested
from skillos.capability_invocation_os.adapters.kill_switch import kill_switch
class TestAdapterConfigStrictness:
    def test_framework_never_enabled(self):
        for s in [None,{},{"ADAPTER_FRAMEWORK_ENABLED":True},{"ADAPTER_FRAMEWORK_ENABLED":1}]: assert is_adapter_framework_enabled(load_config(s)) is False
    def test_non_bool_disabled(self):
        for v in [1,"true","yes",[True],{"x":True}]: c=load_config({"ADAPTER_FRAMEWORK_ENABLED":v}); assert is_requested("_framework_requested",c) is False
    def test_kill_switch_overrides(self): assert kill_switch.overrides_requested(load_config({"ADAPTER_FRAMEWORK_ENABLED":True})) is True
