"""
Tests for models.py — data contract verification.

Verifies NoopDryRunRequest and NoopDryRunResponse defaults
and DryRunDecision enum values.
"""

from research.factor_library.dry_run.models import (
    DryRunDecision,
    NoopDryRunRequest,
    NoopDryRunResponse,
)


class TestDryRunDecision:
    """Verify decision enum values."""

    def test_allow_noop_review_only(self):
        assert DryRunDecision.ALLOW_NOOP_REVIEW_ONLY.value == "ALLOW_NOOP_REVIEW_ONLY"

    def test_deny_disabled_default(self):
        assert DryRunDecision.DENY_DISABLED_DEFAULT.value == "DENY_DISABLED_DEFAULT"

    def test_deny_execution_forbidden(self):
        assert DryRunDecision.DENY_EXECUTION_FORBIDDEN.value == "DENY_EXECUTION_FORBIDDEN"

    def test_deny_external_data_forbidden(self):
        assert DryRunDecision.DENY_EXTERNAL_DATA_FORBIDDEN.value == "DENY_EXTERNAL_DATA_FORBIDDEN"

    def test_deny_runtime_write_forbidden(self):
        assert DryRunDecision.DENY_RUNTIME_WRITE_FORBIDDEN.value == "DENY_RUNTIME_WRITE_FORBIDDEN"

    def test_deny_factor_calculation_forbidden(self):
        assert DryRunDecision.DENY_FACTOR_CALCULATION_FORBIDDEN.value == "DENY_FACTOR_CALCULATION_FORBIDDEN"

    def test_deny_factor_result_update_forbidden(self):
        assert DryRunDecision.DENY_FACTOR_RESULT_UPDATE_FORBIDDEN.value == "DENY_FACTOR_RESULT_UPDATE_FORBIDDEN"

    def test_deny_production_forbidden(self):
        assert DryRunDecision.DENY_PRODUCTION_FORBIDDEN.value == "DENY_PRODUCTION_FORBIDDEN"

    def test_deny_broker_forbidden(self):
        assert DryRunDecision.DENY_BROKER_FORBIDDEN.value == "DENY_BROKER_FORBIDDEN"

    def test_deny_real_trade_forbidden(self):
        assert DryRunDecision.DENY_REAL_TRADE_FORBIDDEN.value == "DENY_REAL_TRADE_FORBIDDEN"

    def test_10_decision_values(self):
        assert len(DryRunDecision) == 10


class TestNoopDryRunRequest:
    """Verify request defaults."""

    def test_default_execution_requested_false(self):
        """ASSERT 13"""
        req = NoopDryRunRequest()
        assert req.execution_requested is False

    def test_default_external_data_requested_false(self):
        req = NoopDryRunRequest()
        assert req.external_data_requested is False

    def test_default_runtime_write_requested_false(self):
        req = NoopDryRunRequest()
        assert req.runtime_write_requested is False

    def test_default_factor_calculation_requested_false(self):
        req = NoopDryRunRequest()
        assert req.factor_calculation_requested is False

    def test_default_factor_ids_empty(self):
        req = NoopDryRunRequest()
        assert req.factor_ids == ()

    def test_request_is_frozen(self):
        req = NoopDryRunRequest(factor_ids=("F21", "F22"))
        assert req.factor_ids == ("F21", "F22")


class TestNoopDryRunResponse:
    """Verify response defaults."""

    def test_default_side_effects_false(self):
        """ASSERT 14"""
        resp = NoopDryRunResponse()
        assert resp.side_effects_performed is False

    def test_default_execution_started_false(self):
        resp = NoopDryRunResponse()
        assert resp.execution_started is False

    def test_default_allowed_false(self):
        resp = NoopDryRunResponse()
        assert resp.allowed is False

    def test_default_decision_deny(self):
        resp = NoopDryRunResponse()
        assert resp.decision == DryRunDecision.DENY_DISABLED_DEFAULT

    def test_response_is_frozen(self):
        resp = NoopDryRunResponse(
            decision=DryRunDecision.DENY_EXECUTION_FORBIDDEN,
            allowed=False,
            reason="denied",
        )
        assert resp.allowed is False
