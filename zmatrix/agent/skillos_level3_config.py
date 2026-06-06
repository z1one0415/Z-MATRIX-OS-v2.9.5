"""Isolated Level 3 configuration. Default disabled. No runtime hook."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillOSLevel3Config:
    enabled: bool
    audit_path: Path
    write_enabled: bool


def is_level3_enabled() -> bool:
    value = os.getenv("SKILLOS_LEVEL3_ENABLED", "false").strip().lower()
    return value in {"1", "true", "yes", "on"}


def get_level3_config(audit_path: str | Path = "runtime_audit/skillos_level3_shadow") -> SkillOSLevel3Config:
    enabled = is_level3_enabled()
    return SkillOSLevel3Config(enabled=enabled, audit_path=Path(audit_path), write_enabled=enabled)
