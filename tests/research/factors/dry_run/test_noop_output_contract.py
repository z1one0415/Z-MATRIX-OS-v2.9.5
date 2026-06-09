"""
Tests for noop_output.py — NOOP_REVIEW_ONLY, no trade fields.
"""

from research.factor_library.dry_run.models import (
    DryRunDecision,
    NoopDryRunRequest,
)
from research.factor_library.dry_run.noop_output import build_noop_output


class TestNoopOutputContract:
    """Verify output structure has zero trade signals."""

    def test_output_mode_noop(self):
        """ASSERT 30"""
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert output["output_mode"] == "NOOP_REVIEW_ONLY"

    def test_no_buy_signal(self):
        """ASSERT 31"""
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "buy_signal" not in output

    def test_no_sell_signal(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "sell_signal" not in output

    def test_no_order_signal(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "order_signal" not in output

    def test_no_position_weight(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "position_weight" not in output

    def test_no_alpha_signal(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "alpha_signal" not in output

    def test_no_expected_return_claim(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "expected_return_claim" not in output

    def test_no_broker_payload(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "broker_payload" not in output

    def test_no_real_trade_payload(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert "real_trade_payload" not in output

    def test_alpha_claim_allowed_false(self):
        """ASSERT 32"""
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert output["alpha_claim_allowed"] is False

    def test_broker_runtime_allowed_false(self):
        """ASSERT 33"""
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert output["broker_runtime_allowed"] is False

    def test_real_trade_allowed_false(self):
        """ASSERT 34"""
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert output["real_trade_allowed"] is False

    def test_trade_signal_allowed_false(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert output["trade_signal_allowed"] is False

    def test_allowed_always_false(self):
        req = NoopDryRunRequest()
        for decision in DryRunDecision:
            output = build_noop_output(req, decision)
            assert output["allowed"] is False

    def test_side_effects_performed_false(self):
        req = NoopDryRunRequest()
        output = build_noop_output(req, DryRunDecision.DENY_DISABLED_DEFAULT)
        assert output["side_effects_performed"] is False
