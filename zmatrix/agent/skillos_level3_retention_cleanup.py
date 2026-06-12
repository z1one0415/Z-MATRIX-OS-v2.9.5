"""Scoped retention cleanup for SkillOS Level 3 audit artifacts."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from zmatrix.agent.skillos_level3_retention_config import SkillOSLevel3RetentionConfig


@dataclass(frozen=True)
class SkillOSLevel3RetentionCleanupResult:
    deleted_paths: list[str]
    deleted_count: int
    refused_paths: list[str]
    refused_count: int
    dry_run: bool
    enabled: bool


def _resolve_existing_or_parent(path: Path) -> Path:
    if path.exists():
        return path.resolve()
    parent = path.parent if path.parent != path else Path(".")
    return parent.resolve() / path.name


def _is_forbidden_audit_root(audit_path: Path, forbidden_paths: tuple[str, ...]) -> bool:
    audit = _resolve_existing_or_parent(audit_path)
    cwd = Path.cwd().resolve()
    for raw in forbidden_paths:
        forbidden = (cwd / raw).resolve()
        if audit == forbidden or forbidden in audit.parents:
            return True
    return False


def _within(base: Path, candidate: Path) -> bool:
    base_resolved = base.resolve()
    candidate_resolved = candidate.resolve()
    return candidate_resolved == base_resolved or base_resolved in candidate_resolved.parents


def run_retention_cleanup(
    config: SkillOSLevel3RetentionConfig,
    *,
    apply: bool = False,
) -> SkillOSLevel3RetentionCleanupResult:
    audit_path = config.audit_path
    if not audit_path.exists() or not audit_path.is_dir():
        return SkillOSLevel3RetentionCleanupResult([], 0, [], 0, dry_run=not apply, enabled=config.enabled)

    if _is_forbidden_audit_root(audit_path, config.forbidden_cleanup_paths):
        return SkillOSLevel3RetentionCleanupResult(
            [],
            0,
            [str(audit_path)],
            1,
            dry_run=not apply,
            enabled=config.enabled,
        )

    cutoff = time.time() - config.retention_days * 86400
    candidates: list[Path] = []
    refused: list[str] = []

    for path in sorted(audit_path.rglob("*")):
        if not path.is_file():
            continue
        if not _within(audit_path, path):
            refused.append(str(path))
            continue
        if path.stat().st_mtime < cutoff:
            candidates.append(path)

    deleted_paths = [str(path) for path in candidates]
    if apply and config.enabled:
        for path in candidates:
            path.unlink(missing_ok=True)

    return SkillOSLevel3RetentionCleanupResult(
        deleted_paths=deleted_paths,
        deleted_count=len(deleted_paths) if apply and config.enabled else 0,
        refused_paths=refused,
        refused_count=len(refused),
        dry_run=not apply,
        enabled=config.enabled,
    )
