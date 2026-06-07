"""
Level 4 guards: enable/disable determination.

All guards return False for any failure. Default is disabled.
No env-var bypass. No production config path.
"""

from skillos.level4.config import Level4Config, load_config
from skillos.level4.models import Level4EvaluationResult


def is_level4_enabled(config: Level4Config) -> bool:
    """
    Check whether Level 4 warning capability is enabled.

    Returns False for any error, missing data, or non-bool-true value.
    """
    try:
        return getattr(config, "warning_enabled", False) is True
    except Exception:
        return False


def should_emit_warning(config: Level4Config) -> bool:
    """
    Whether Level 4 should emit warnings through side channels.

    All sub-controls must be explicitly enabled. Default False.
    """
    try:
        return (
            getattr(config, "warning_enabled", False) is True
            and getattr(config, "audit_file_enabled", False) is True
            and getattr(config, "operator_report_enabled", False) is True
        )
    except Exception:
        return False


def disabled_guard(config: Level4Config) -> Level4EvaluationResult:
    """
    Early return disabled result if Level 4 is not fully enabled.

    Returns an empty, CONTINUE result with no side effects.
    """
    return Level4EvaluationResult(action="CONTINUE", warnings=[], disabled=True)
