"""Tests for FactorLibraryFixtureProvider — 9 tests."""

import inspect

from skillos.capability_invocation_os.adapters.factor_library.fixture_provider import (
    FactorLibraryFixtureProvider,
)
from skillos.capability_invocation_os.adapters.factor_library.fixtures import (
    ALL_FIXTURE_SCENARIOS,
    FIXTURE_FACTOR_SAFE_VALIDATED,
    FIXTURE_FACTOR_DENIED_PIT_FAILED,
    FIXTURE_FACTOR_DENIED_COVERAGE_FAILED,
    FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED,
    FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED,
    FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorAdapterDecision,
)


def _provider():
    return FactorLibraryFixtureProvider()


def test_list_fixture_factors_returns_only_fake():
    """All fixture factors must use FAKE_ prefix."""
    provider = _provider()
    resp = provider.list_fixture_factors()
    assert resp.decision in (
        FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        FactorAdapterDecision.ALLOW_REGISTRY_ONLY,
    )
    # Verify all scenarios use FAKE_ factor IDs
    for scenario in ALL_FIXTURE_SCENARIOS:
        assert scenario.factor_id.startswith("FAKE_FACTOR_"), (
            f"Expected FAKE_ prefix, got {scenario.factor_id}"
        )


def test_provider_never_reads_research():
    """Provider source must not contain research imports."""
    import skillos.capability_invocation_os.adapters.factor_library.fixture_provider as mod
    source = inspect.getsource(mod)
    assert "import research" not in source
    assert "from research" not in source
    assert "research.factor_library" not in source


def test_unknown_factor_returns_deny_not_found():
    """Unknown factor_id must return DENY_FACTOR_NOT_FOUND."""
    provider = _provider()
    resp = provider.get_fixture_profile("NONEXISTENT_FACTOR_999")
    assert resp.decision == FactorAdapterDecision.DENY_FACTOR_NOT_FOUND


def test_safe_fixture_returns_readonly_allow():
    """FIXTURE_FACTOR_SAFE_VALIDATED must return ALLOW_READONLY_CONTEXT."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    assert resp.decision == FactorAdapterDecision.ALLOW_READONLY_CONTEXT


def test_pit_failed_returns_deny():
    """FIXTURE_FACTOR_DENIED_PIT_FAILED must return DENY_PIT_FAILED."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_PIT_FAILED.factor_id)
    assert resp.decision == FactorAdapterDecision.DENY_PIT_FAILED


def test_coverage_failed_returns_deny():
    """FIXTURE_FACTOR_DENIED_COVERAGE_FAILED must return DENY_COVERAGE_FAILED."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_COVERAGE_FAILED.factor_id)
    assert resp.decision == FactorAdapterDecision.DENY_COVERAGE_FAILED


def test_guardrail_failed_returns_deny():
    """FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED must return DENY_GUARDRAIL_FAILED."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED.factor_id)
    assert resp.decision == FactorAdapterDecision.DENY_GUARDRAIL_FAILED


def test_promotion_not_allowed_returns_deny():
    """FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED must return DENY_PROMOTION_NOT_ALLOWED."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED.factor_id)
    assert resp.decision == FactorAdapterDecision.DENY_PROMOTION_NOT_ALLOWED


def test_execution_forbidden_returns_deny():
    """FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN must return DENY_EXECUTION_FORBIDDEN."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN.factor_id)
    assert resp.decision == FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN
