"""
Noop Output — Produce a NOOP_REVIEW_ONLY output structure.

Contains NO trade signals, NO alpha claims, NO broker payloads.
Output is purely an in-memory dict.
"""

from __future__ import annotations

from .models import DryRunDecision, NoopDryRunRequest


def build_noop_output(
    request: NoopDryRunRequest,
    decision: DryRunDecision,
) -> dict:
    """
    Build a noop output dict from a request and decision.

    The output is purely observational — no trade signals, no
    alpha claims, no broker/production/real_trade payloads.

    Args:
        request: The original noop dry-run request.
        decision: The guard evaluation decision.

    Returns:
        A dict with NOOP_REVIEW_ONLY fields. No trade fields present.
    """
    return {
        "output_mode": "NOOP_REVIEW_ONLY",
        "allowed": False,
        "decision": decision.value,
        "side_effects_performed": False,
        "execution_started": False,
        "trade_signal_allowed": False,
        "alpha_claim_allowed": False,
        "broker_runtime_allowed": False,
        "real_trade_allowed": False,
    }
