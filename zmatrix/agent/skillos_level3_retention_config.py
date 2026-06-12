"""Retention configuration for SkillOS Level 3 audit artifacts.

The cleanup surface is intentionally narrow: callers must pass an explicit
audit directory, and repository/runtime roots are refused even when apply=True.
"""

from dataclasses import dataclass
from pathlib import Path


FORBIDDEN_CLEANUP_PATHS = (
    ".",
    ".git",
    "data",
    "runtime_reports",
    "runtime_audit",
    "research",
    "scripts",
    "skillos",
    "tests",
    "zmatrix",
)


@dataclass(frozen=True)
class SkillOSLevel3RetentionConfig:
    audit_path: Path
    retention_days: int
    enabled: bool
    forbidden_cleanup_paths: tuple[str, ...] = FORBIDDEN_CLEANUP_PATHS


def get_default_retention_config(
    audit_path: str | Path,
    *,
    retention_days: int = 14,
    enabled: bool = True,
) -> SkillOSLevel3RetentionConfig:
    return SkillOSLevel3RetentionConfig(
        audit_path=Path(audit_path),
        retention_days=retention_days,
        enabled=enabled,
    )
