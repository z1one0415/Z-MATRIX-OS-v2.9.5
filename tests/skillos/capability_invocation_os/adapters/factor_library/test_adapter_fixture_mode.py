"""Tests for adapter fixture_mode — 7 tests."""

from unittest.mock import patch

from skillos.capability_invocation_os.adapters.factor_library.adapter import (
    FactorLibraryReadOnlyAdapter,
)
from skillos.capability_invocation_os.adapters.factor_library.fixture_provider import (
    FactorLibraryFixtureProvider,
)
from skillos.capability_invocation_os.adapters.factor_library.fixtures import (
    FIXTURE_FACTOR_SAFE_VALIDATED,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorAdapterDecision,
    FactorFilter,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS
from skillos.capability_invocation_os.adapters.factor_library.config import (
    is_factor_library_adapter_enabled,
    is_runtime_enabled,
)


def test_default_adapter_still_disabled_noop():
    """Default adapter (no fixture_mode) must return DISABLED_DEFAULT_NOOP."""
    adapter = FactorLibraryReadOnlyAdapter()
    resp = adapter.list_factors()
    assert resp.decision == FactorAdapterDecision.DISABLED_DEFAULT_NOOP


def test_fixture_mode_false_ignores_provider():
    """fixture_mode=False must ignore fixture_provider even if provided."""
    provider = FactorLibraryFixtureProvider()
    adapter = FactorLibraryReadOnlyAdapter(fixture_provider=provider, fixture_mode=False)
    resp = adapter.get_factor_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    assert resp.decision == FactorAdapterDecision.DISABLED_DEFAULT_NOOP


@patch(
    "skillos.capability_invocation_os.adapters.factor_library.adapter.should_force_disabled",
    return_value=True,
)
def test_kill_switch_overrides_fixture_mode(mock_kill):
    """Kill switch active must override fixture_mode=True."""
    provider = FactorLibraryFixtureProvider()
    adapter = FactorLibraryReadOnlyAdapter(fixture_provider=provider, fixture_mode=True)
    resp = adapter.get_factor_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    assert resp.decision == FactorAdapterDecision.DISABLED_DEFAULT_NOOP


@patch(
    "skillos.capability_invocation_os.adapters.factor_library.adapter.should_force_disabled",
    return_value=False,
)
def test_fixture_mode_true_returns_fixture_response(mock_kill):
    """fixture_mode=True with provider must return fixture decisions."""
    provider = FactorLibraryFixtureProvider()
    adapter = FactorLibraryReadOnlyAdapter(fixture_provider=provider, fixture_mode=True)
    resp = adapter.get_factor_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    assert resp.decision == FactorAdapterDecision.ALLOW_READONLY_CONTEXT


@patch(
    "skillos.capability_invocation_os.adapters.factor_library.adapter.should_force_disabled",
    return_value=False,
)
def test_fixture_response_no_alpha_trade_weight(mock_kill):
    """Fixture responses must have all forbidden outputs removed."""
    provider = FactorLibraryFixtureProvider()
    adapter = FactorLibraryReadOnlyAdapter(fixture_provider=provider, fixture_mode=True)
    resp = adapter.get_factor_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    # All BLOCKED_OUTPUTS must be listed as removed
    assert set(resp.forbidden_outputs_removed) == set(BLOCKED_OUTPUTS)


@patch(
    "skillos.capability_invocation_os.adapters.factor_library.adapter.should_force_disabled",
    return_value=False,
)
def test_no_runtime_enablement_flag_changes(mock_kill):
    """fixture_mode must not change config.is_runtime_enabled()."""
    provider = FactorLibraryFixtureProvider()
    # Before
    assert is_runtime_enabled() is False
    # Create adapter with fixture mode
    adapter = FactorLibraryReadOnlyAdapter(fixture_provider=provider, fixture_mode=True)
    _ = adapter.get_factor_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    # After — runtime must still be disabled
    assert is_runtime_enabled() is False


@patch(
    "skillos.capability_invocation_os.adapters.factor_library.adapter.should_force_disabled",
    return_value=False,
)
def test_all_enabled_functions_remain_false(mock_kill):
    """All config enabled functions must remain False after fixture_mode usage."""
    provider = FactorLibraryFixtureProvider()
    adapter = FactorLibraryReadOnlyAdapter(fixture_provider=provider, fixture_mode=True)
    _ = adapter.list_factors()
    _ = adapter.get_factor_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)

    # All config functions must still return False
    from skillos.capability_invocation_os.adapters.factor_library import config
    assert config.is_factor_library_adapter_enabled() is False
    assert config.is_factor_read_enabled() is False
    assert config.is_factor_evidence_read_enabled() is False
    assert config.is_candidate_monitor_enabled() is False
    assert config.is_research_context_enabled() is False
    assert config.is_runtime_enabled() is False
    assert config.is_adapter_execution_enabled() is False
    assert config.is_capability_execution_enabled() is False
