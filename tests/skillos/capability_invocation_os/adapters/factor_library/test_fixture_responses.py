"""Tests for fixture responses — 6 tests."""

from skillos.capability_invocation_os.adapters.factor_library.fixture_provider import (
    FactorLibraryFixtureProvider,
)
from skillos.capability_invocation_os.adapters.factor_library.fixtures import (
    ALL_FIXTURE_SCENARIOS,
    FIXTURE_FACTOR_SAFE_VALIDATED,
    FIXTURE_FACTOR_DENIED_PIT_FAILED,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorAdapterDecision,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS


def _provider():
    return FactorLibraryFixtureProvider()


def _all_responses():
    """Get responses for all fixture scenarios."""
    provider = _provider()
    responses = []
    for scenario in ALL_FIXTURE_SCENARIOS:
        resp = provider.get_fixture_profile(scenario.factor_id)
        responses.append(resp)
    return responses


def test_all_responses_have_no_real_source_flag():
    """All responses must signal no_real_source via evidence source_commit."""
    for resp in _all_responses():
        assert resp.evidence is not None
        assert resp.evidence.source_commit == "P1_FIXTURE_ONLY"


def test_all_responses_have_fixture_source_commit():
    """All responses must have fixture_source_commit = P1_FIXTURE_ONLY."""
    for resp in _all_responses():
        assert resp.evidence.source_commit == "P1_FIXTURE_ONLY"


def test_all_responses_have_source_class_fixture():
    """All responses must have source_class = factor_library_fixture."""
    for resp in _all_responses():
        assert resp.evidence.source_class == "factor_library_fixture"


def test_all_responses_remove_forbidden_outputs():
    """All responses must have forbidden_outputs_removed populated with BLOCKED_OUTPUTS."""
    for resp in _all_responses():
        assert set(resp.forbidden_outputs_removed) == set(BLOCKED_OUTPUTS)


def test_safe_fixture_no_alpha_trade_weight():
    """Safe fixture response must not contain alpha/trade/weight signals."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_SAFE_VALIDATED.factor_id)
    forbidden_in_response = {"alpha_claim", "buy_signal", "sell_signal", "position_weight"}
    # The forbidden outputs removed list confirms they were stripped
    assert forbidden_in_response.issubset(set(resp.forbidden_outputs_removed))


def test_denied_fixture_cannot_become_valid():
    """A denied fixture must never transition to ALLOW decisions."""
    provider = _provider()
    resp = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_PIT_FAILED.factor_id)
    assert resp.decision == FactorAdapterDecision.DENY_PIT_FAILED
    # Calling again must produce same result (no state mutation)
    resp2 = provider.get_fixture_profile(FIXTURE_FACTOR_DENIED_PIT_FAILED.factor_id)
    assert resp2.decision == FactorAdapterDecision.DENY_PIT_FAILED
    assert resp2.decision.value.startswith("DENY_")
