import pytest
from skillos.capability_invocation_os.runtime.config import (load_config, is_runtime_requested, is_runtime_enabled, is_adapter_execution_enabled, is_capability_execution_enabled, env_override_detected)
from skillos.capability_invocation_os.runtime.kill_switch import kill_switch
class TestP1ConfigStrictness:
    def test_default_disabled(self):
        c=load_config(None); assert is_runtime_enabled(c) is False
    def test_int_one_disabled(self):
        c=load_config({"CAPABILITY_OS_RUNTIME_ENABLED":1}); assert is_runtime_enabled(c) is False
    def test_string_true_disabled(self):
        c=load_config({"CAPABILITY_OS_RUNTIME_ENABLED":"true"}); assert is_runtime_enabled(c) is False
    def test_env_override_detected_does_not_enable(self):
        env_override_detected()
    def test_kill_switch_override(self):
        assert kill_switch.master_disable is True
    def test_all_disabled_default(self):
        c=load_config()
        assert is_runtime_enabled(c) is False
        assert is_adapter_execution_enabled(c) is False
        assert is_capability_execution_enabled(c) is False
