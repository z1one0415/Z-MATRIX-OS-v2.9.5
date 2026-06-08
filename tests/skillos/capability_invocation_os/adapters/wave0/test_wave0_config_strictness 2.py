from skillos.capability_invocation_os.adapters.wave0.config import load,is_wave0_enabled
from skillos.capability_invocation_os.adapters.wave0.kill_switch import ks
class TestConfig:
    def test_never_enabled(self):
        for s in [None,{},{"WAVE0_READONLY_ADAPTERS_ENABLED":True},{"WAVE0_READONLY_ADAPTERS_ENABLED":1}]: assert is_wave0_enabled(load(s)) is False
    def test_kill_switch(self):
        k = ks()
        assert k.overrides(load({"WAVE0_READONLY_ADAPTERS_ENABLED":True})) is True
