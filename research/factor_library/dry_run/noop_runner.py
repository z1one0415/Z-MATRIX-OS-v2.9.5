"""
Noop Runner — The controlled noop dry-run P0 runner.

Always disabled by default. Never executes real dry-run.
Never calculates factors. Never writes files. Never fetches data.
"""

from __future__ import annotations

from . import hash_evidence, safety_guard
from .models import (
    DryRunDecision,
    NoopDryRunRequest,
    NoopDryRunResponse,
)


class ControlledNoopDryRunRunner:
    """
    The P0 controlled noop dry-run runner.

    In disabled-default mode, ALL operations are denied. This class
    serves as the skeleton for future controlled execution, but in
    P0 it always returns DENY_DISABLED_DEFAULT with zero side effects.

    There is NO execute/call/invoke method — only `run` which always
    denies and returns a noop response.
    """

    def run(self, request: NoopDryRunRequest) -> NoopDryRunResponse:
        """
        Process a noop dry-run request.

        This method:
        1. Evaluates the request through the safety guard
        2. NEVER executes real dry-run
        3. NEVER calculates factors
        4. NEVER writes files
        5. NEVER fetches external data
        6. ALWAYS returns allowed=False
        7. ALWAYS returns side_effects_performed=False
        8. ALWAYS returns execution_started=False

        Args:
            request: The noop dry-run request to evaluate.

        Returns:
            A NoopDryRunResponse with denied decision and zero side effects.
        """
        decision = safety_guard.evaluate_request(request)

        # Compute a hash of the denial payload for evidence (no persistence)
        denial_payload = {
            "decision": decision.value,
            "factor_ids": list(request.factor_ids),
            "requested_operation": request.requested_operation,
        }
        output_hash = hash_evidence.compute_hash_only_evidence(denial_payload)

        return NoopDryRunResponse(
            decision=decision,
            allowed=False,
            reason=f"Request denied: {decision.value}",
            noop_output_hash=output_hash,
            side_effects_performed=False,
            execution_started=False,
        )
