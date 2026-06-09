"""
Tests for safety_guard.py — Denies all forbidden operations.
"""

from research.factor_library.dry_run.models import (
    DryRunDecision,
    NoopDryRunRequest,
)
from research.factor_library.dry_run.safety_guard import (
    assert_no_side_effects_allowed,
    evaluate_request,
    guard_summary,
)


class TestSafetyGuardDenies:
    """Verify all denies work correctly."""

    def test_denies_disabled_default(self):
        """ASSERT 15"""
        req = NoopDryRunRequest()
        assert evaluate_request(req) == DryRunDecision.DENY_DISABLED_DEFAULT

    def test_denies_execution_requested(self):
        """ASSERT 16"""
        req = NoopDryRunRequest(execution_requested=True)
        assert evaluate_request(req) == DryRunDecision.DENY_EXECUTION_FORBIDDEN

    def test_denies_external_data(self):
        """ASSERT 17"""
        req = NoopDryRunRequest(external_data_requested=True)
        assert evaluate_request(req) == DryRunDecision.DENY_EXTERNAL_DATA_FORBIDDEN

    def test_denies_runtime_write(self):
        """ASSERT 18"""
        req = NoopDryRunRequest(runtime_write_requested=True)
        assert evaluate_request(req) == DryRunDecision.DENY_RUNTIME_WRITE_FORBIDDEN

    def test_denies_factor_calculation(self):
        """ASSERT 19"""
        req = NoopDryRunRequest(factor_calculation_requested=True)
        assert evaluate_request(req) == DryRunDecision.DENY_FACTOR_CALCULATION_FORBIDDEN

    def test_denies_all_forbidden_combined(self):
        req = NoopDryRunRequest(
            execution_requested=True,
            external_data_requested=True,
            runtime_write_requested=True,
        )
        assert evaluate_request(req) == DryRunDecision.DENY_EXECUTION_FORBIDDEN

    def test_normal_request_denied(self):
        req = NoopDryRunRequest(
            factor_ids=("F21", "F22"),
            requested_operation="noop_review",
        )
        assert evaluate_request(req) == DryRunDecision.DENY_DISABLED_DEFAULT


class TestGuardSummary:
    """Verify guard summary returns all false."""

    def test_all_false_by_default(self):
        summary = guard_summary()
        for key, value in summary.items():
            assert value is False, f"{key} should be False, got {value}"

    def test_assert_no_side_effects_false(self):
        assert assert_no_side_effects_allowed() is False


class TestNoSideEffects:
    """Verify safety_guard has no side effects."""

    def test_evaluate_request_no_raises(self):
        """Should never raise on any input."""
        req = NoopDryRunRequest()
        result = evaluate_request(req)
        assert isinstance(result, DryRunDecision)
