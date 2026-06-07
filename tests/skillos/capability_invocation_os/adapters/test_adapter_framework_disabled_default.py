import pytest
from skillos.capability_invocation_os.adapters.config import load_config, is_adapter_framework_enabled, is_adapter_registration_enabled, is_adapter_execution_enabled, is_zmatrix_module_adapters_enabled, env_override_detected
from skillos.capability_invocation_os.adapters.base import AdapterBase
from skillos.capability_invocation_os.adapters.kill_switch import kill_switch
class TestAdapterFrameworkDisabledDefault:
    def test_framework_disabled(self): assert is_adapter_framework_enabled(load_config()) is False
    def test_registration_disabled(self): assert is_adapter_registration_enabled(load_config()) is False
    def test_execution_disabled(self): assert is_adapter_execution_enabled(load_config()) is False
    def test_zmatrix_disabled(self): assert is_zmatrix_module_adapters_enabled(load_config()) is False
    def test_env_not_enabling(self): assert env_override_detected() is False
    def test_kill_switch_master(self): assert kill_switch.master_disable is True
    def test_base_deny(self): assert AdapterBase().deny().action == "DENY"
