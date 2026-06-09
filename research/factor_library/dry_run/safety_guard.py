"""
Safety Guard — Evaluates requests and denies all forbidden operations.

No network. No file I/O. No side effects. Always denies in disabled-default.
"""

from __future__ import annotations

from . import config
from .models import DryRunDecision, NoopDryRunRequest


def evaluate_request(request: NoopDryRunRequest) -> DryRunDecision:
    """
    Evaluate a noop dry-run request against safety rules.

    Priority order:
    1. If runner is disabled → DENY_DISABLED_DEFAULT
    2. Forbidden operations detected → specific deny
    3. Default fallback → DENY_DISABLED_DEFAULT
    """
    # Guard 1: Execution is never allowed
    if request.execution_requested:
        return DryRunDecision.DENY_EXECUTION_FORBIDDEN

    # Guard 2: External data is never allowed
    if request.external_data_requested:
        return DryRunDecision.DENY_EXTERNAL_DATA_FORBIDDEN

    # Guard 3: Runtime write is never allowed
    if request.runtime_write_requested:
        return DryRunDecision.DENY_RUNTIME_WRITE_FORBIDDEN

    # Guard 4: Factor calculation is never allowed
    if request.factor_calculation_requested:
        return DryRunDecision.DENY_FACTOR_CALCULATION_FORBIDDEN

    # Guard 5: Runner must be enabled for any noop review
    if not config.is_runner_enabled():
        return DryRunDecision.DENY_DISABLED_DEFAULT

    # Default: deny
    return DryRunDecision.DENY_DISABLED_DEFAULT


def assert_no_side_effects_allowed() -> bool:
    """Hard assertion: side effects are never allowed."""
    return False


def guard_summary() -> dict:
    """Return a summary of all guard states (all false in disabled-default)."""
    return {
        "runner_enabled": config.is_runner_enabled(),
        "execution_allowed": config.is_execution_allowed(),
        "side_effects_allowed": config.are_side_effects_allowed(),
        "runtime_reports_write_allowed": config.is_runtime_reports_write_allowed(),
        "runtime_audit_write_allowed": config.is_runtime_audit_write_allowed(),
        "external_data_fetch_allowed": config.is_external_data_fetch_allowed(),
        "factor_calculation_allowed": config.is_factor_calculation_allowed(),
        "factor_result_update_allowed": config.is_factor_result_update_allowed(),
        "production_allowed": config.is_production_allowed(),
        "broker_runtime_allowed": config.is_broker_runtime_allowed(),
        "real_trade_allowed": config.is_real_trade_allowed(),
    }
