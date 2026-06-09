import pytest
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.config import (
    is_a1_factor_bridge_enabled,
    is_zmatrix_module_call_enabled,
    is_runtime_enabled,
    is_adapter_execution_enabled,
    is_capability_execution_enabled,
    is_real_factor_call_enabled,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.kill_switch import (
    is_master_kill_switch_active,
    is_a1_bridge_kill_switch_active,
    is_factor_bridge_kill_switch_active,
    should_force_disabled,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.bridge import A1FactorLibraryBridge


def test_all_a1_bridge_enabled_false():
    assert is_a1_factor_bridge_enabled() is False
    assert is_zmatrix_module_call_enabled() is False
    assert is_runtime_enabled() is False
    assert is_adapter_execution_enabled() is False
    assert is_capability_execution_enabled() is False
    assert is_real_factor_call_enabled() is False


def test_all_kill_switches_active():
    assert is_master_kill_switch_active() is True
    assert is_a1_bridge_kill_switch_active() is True
    assert is_factor_bridge_kill_switch_active() is True
    assert should_force_disabled() is True


def test_default_bridge_returns_disabled_noop():
    bridge = A1FactorLibraryBridge()
    resp = bridge.bridge_factor_response(None)
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"
    assert resp.degraded is True


def test_fixture_mode_false_returns_disabled_noop():
    from skillos.capability_invocation_os.adapters.factor_library.fixture_provider import (
        FactorLibraryFixtureProvider,
    )
    provider = FactorLibraryFixtureProvider()
    bridge = A1FactorLibraryBridge(factor_adapter=provider, fixture_mode=False)
    resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"


def test_no_factor_adapter_returns_disabled_noop():
    bridge = A1FactorLibraryBridge(factor_adapter=None, fixture_mode=True)
    resp = bridge.bridge_factor_profile("FAKE_FACTOR_001")
    assert resp.decision.value == "DISABLED_DEFAULT_NOOP"
