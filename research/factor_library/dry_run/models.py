"""
Data models for the controlled noop dry-run P0.

Pure dataclass types — no network, no file I/O, no side effects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DryRunDecision(str, Enum):
    """Decision outcomes for the noop dry-run guard."""
    ALLOW_NOOP_REVIEW_ONLY = "ALLOW_NOOP_REVIEW_ONLY"
    DENY_DISABLED_DEFAULT = "DENY_DISABLED_DEFAULT"
    DENY_EXECUTION_FORBIDDEN = "DENY_EXECUTION_FORBIDDEN"
    DENY_EXTERNAL_DATA_FORBIDDEN = "DENY_EXTERNAL_DATA_FORBIDDEN"
    DENY_RUNTIME_WRITE_FORBIDDEN = "DENY_RUNTIME_WRITE_FORBIDDEN"
    DENY_FACTOR_CALCULATION_FORBIDDEN = "DENY_FACTOR_CALCULATION_FORBIDDEN"
    DENY_FACTOR_RESULT_UPDATE_FORBIDDEN = "DENY_FACTOR_RESULT_UPDATE_FORBIDDEN"
    DENY_PRODUCTION_FORBIDDEN = "DENY_PRODUCTION_FORBIDDEN"
    DENY_BROKER_FORBIDDEN = "DENY_BROKER_FORBIDDEN"
    DENY_REAL_TRADE_FORBIDDEN = "DENY_REAL_TRADE_FORBIDDEN"


@dataclass(frozen=True)
class NoopDryRunRequest:
    """A request to the noop dry-run runner."""
    factor_ids: tuple[str, ...] = field(default_factory=tuple)
    requested_operation: str = "noop_review"
    execution_requested: bool = False
    external_data_requested: bool = False
    runtime_write_requested: bool = False
    factor_calculation_requested: bool = False


@dataclass(frozen=True)
class NoopDryRunResponse:
    """A response from the noop dry-run runner."""
    decision: DryRunDecision = DryRunDecision.DENY_DISABLED_DEFAULT
    allowed: bool = False
    reason: str = "Runner is disabled by default"
    noop_output_hash: str | None = None
    side_effects_performed: bool = False
    execution_started: bool = False
