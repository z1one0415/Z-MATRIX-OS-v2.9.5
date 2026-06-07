"""
Level 4 disabled-by-default configuration.

All config keys default to false. Any config parse failure = disabled.
No env-var override bypass. No production/broker/real_trade config reading.
"""

import os
from dataclasses import dataclass
from typing import Optional


# Sentinel for "config not found"
_UNSET = object()


@dataclass(frozen=True)
class Level4Config:
    """Immutable Level 4 configuration with fail-safe defaults."""

    warning_enabled: bool = False
    audit_file_enabled: bool = False
    operator_report_enabled: bool = False


def load_config(source: Optional[dict] = None) -> Level4Config:
    """
    Load Level 4 config from an optional dict source.

    Rules:
    - source=None or empty → all disabled (safe default)
    - missing key → disabled for that key
    - unreadable/malformed → disabled for that key
    - unknown value type → disabled for that key
    - bool True only enables; anything else (1, "yes", None) → disabled

    This isolates Level 4 from all production/broker/real_trade config paths.
    """
    if source is None or not isinstance(source, dict):
        return Level4Config()

    cfg = {}
    for key, default_val in [
        ("LEVEL4_WARNING_ENABLED", False),
        ("LEVEL4_AUDIT_FILE_ENABLED", False),
        ("LEVEL4_OPERATOR_REPORT_ENABLED", False),
    ]:
        raw = source.get(key, _UNSET)
        if raw is _UNSET:
            cfg[key] = False
        elif isinstance(raw, bool):
            cfg[key] = raw
        else:
            # Anything other than bool True is treated as False
            cfg[key] = False

    return Level4Config(
        warning_enabled=cfg.get("LEVEL4_WARNING_ENABLED", False),
        audit_file_enabled=cfg.get("LEVEL4_AUDIT_FILE_ENABLED", False),
        operator_report_enabled=cfg.get("LEVEL4_OPERATOR_REPORT_ENABLED", False),
    )


def env_override_disabled() -> bool:
    """
    Safety check: no environment variable can enable Level 4.

    Returns True if any env-based enable attempt is detected.
    This is a safeguard, not an enable path.
    """
    env_keys = [
        "LEVEL4_WARNING_ENABLED",
        "LEVEL4_AUDIT_FILE_ENABLED",
        "LEVEL4_OPERATOR_REPORT_ENABLED",
    ]
    for key in env_keys:
        val = os.environ.get(key)
        if val is not None and val.strip().lower() in ("true", "1", "yes", "on"):
            return True  # env override attempt detected
    return False
