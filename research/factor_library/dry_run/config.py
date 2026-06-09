"""
Configuration — All runtime flags hard-coded to False.

No environment variable reads. No config file reads. No overrides.
This is the disabled-default safety baseline.
"""

# All runtime capabilities are DISABLED by default
RUNNER_ENABLED: bool = False
EXECUTION_ALLOWED: bool = False
SIDE_EFFECTS_ALLOWED: bool = False
RUNTIME_REPORTS_WRITE_ALLOWED: bool = False
RUNTIME_AUDIT_WRITE_ALLOWED: bool = False
EXTERNAL_DATA_FETCH_ALLOWED: bool = False
FACTOR_CALCULATION_ALLOWED: bool = False
FACTOR_RESULT_UPDATE_ALLOWED: bool = False
PRODUCTION_ALLOWED: bool = False
BROKER_RUNTIME_ALLOWED: bool = False
REAL_TRADE_ALLOWED: bool = False


def is_runner_enabled() -> bool:
    """Runner is always disabled in P0 disabled-default."""
    return False


def is_execution_allowed() -> bool:
    """Execution is never allowed in disabled-default."""
    return False


def are_side_effects_allowed() -> bool:
    """Side effects are never allowed in disabled-default."""
    return False


def is_runtime_reports_write_allowed() -> bool:
    """Runtime report writes are never allowed."""
    return False


def is_runtime_audit_write_allowed() -> bool:
    """Runtime audit writes are never allowed."""
    return False


def is_external_data_fetch_allowed() -> bool:
    """External data fetch is never allowed."""
    return False


def is_factor_calculation_allowed() -> bool:
    """Factor calculation is never allowed."""
    return False


def is_factor_result_update_allowed() -> bool:
    """Factor result updates are never allowed."""
    return False


def is_production_allowed() -> bool:
    """Production is never allowed."""
    return False


def is_broker_runtime_allowed() -> bool:
    """Broker runtime is never allowed."""
    return False


def is_real_trade_allowed() -> bool:
    """Real trade is never allowed."""
    return False
