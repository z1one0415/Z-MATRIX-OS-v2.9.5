import pytest
from skillos.capability_invocation_os.adapters.factor_library.config import (
    is_factor_library_adapter_enabled, is_factor_read_enabled,
    is_runtime_enabled, is_adapter_execution_enabled, is_capability_execution_enabled,
)
from skillos.capability_invocation_os.adapters.factor_library.kill_switch import (
    is_master_kill_switch_active, should_force_disabled,
)
from skillos.capability_invocation_os.adapters.factor_library.adapter import FactorLibraryReadOnlyAdapter

def test_all_enabled_false():
    assert is_factor_library_adapter_enabled() is False
    assert is_factor_read_enabled() is False
    assert is_runtime_enabled() is False
    assert is_adapter_execution_enabled() is False
    assert is_capability_execution_enabled() is False

def test_all_kill_switches_active():
    assert is_master_kill_switch_active() is True
    assert should_force_disabled() is True

def test_adapter_returns_disabled():
    adapter = FactorLibraryReadOnlyAdapter()
    resp = adapter.list_factors(None)
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"
    assert resp.degraded is True

def test_adapter_get_factor_profile_disabled():
    adapter = FactorLibraryReadOnlyAdapter()
    resp = adapter.get_factor_profile("F21")
    assert resp.degraded is True
