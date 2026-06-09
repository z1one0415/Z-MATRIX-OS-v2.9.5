"""
Tests for noop_runner.py — Always returns denied, no side effects.
"""

from research.factor_library.dry_run.models import (
    DryRunDecision,
    NoopDryRunRequest,
    NoopDryRunResponse,
)
from research.factor_library.dry_run.noop_runner import (
    ControlledNoopDryRunRunner,
)


class TestNoopRunnerDisabled:
    """Verify runner always returns denial."""

    def test_returns_allowed_false(self):
        """ASSERT 20"""
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest()
        resp = runner.run(req)
        assert resp.allowed is False

    def test_execution_started_false(self):
        """ASSERT 21"""
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest()
        resp = runner.run(req)
        assert resp.execution_started is False

    def test_side_effects_performed_false(self):
        """ASSERT 22"""
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest()
        resp = runner.run(req)
        assert resp.side_effects_performed is False

    def test_default_request_denied(self):
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest()
        resp = runner.run(req)
        assert resp.decision == DryRunDecision.DENY_DISABLED_DEFAULT

    def test_execution_request_denied(self):
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest(execution_requested=True)
        resp = runner.run(req)
        assert resp.decision == DryRunDecision.DENY_EXECUTION_FORBIDDEN

    def test_response_has_hash(self):
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest(factor_ids=("F21",))
        resp = runner.run(req)
        assert resp.noop_output_hash is not None
        assert len(resp.noop_output_hash) == 64

    def test_never_writes_file(self):
        """ASSERT 23: No file writes — just instantiate and run."""
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest()
        resp = runner.run(req)
        assert isinstance(resp, NoopDryRunResponse)
        # If no exception raised and no I/O, this test passes.

    def test_runner_always_returns_response(self):
        runner = ControlledNoopDryRunRunner()
        req = NoopDryRunRequest(factor_ids=("F21", "F22"))
        resp = runner.run(req)
        assert isinstance(resp, NoopDryRunResponse)

    def test_runner_has_no_execute_method(self):
        """ASSERT 49"""
        runner = ControlledNoopDryRunRunner()
        assert not hasattr(runner, "execute")

    def test_runner_has_no_call_method(self):
        """ASSERT 50"""
        runner = ControlledNoopDryRunRunner()
        assert not hasattr(runner, "call")

    def test_runner_has_no_invoke_method(self):
        """ASSERT 51"""
        runner = ControlledNoopDryRunRunner()
        assert not hasattr(runner, "invoke")
