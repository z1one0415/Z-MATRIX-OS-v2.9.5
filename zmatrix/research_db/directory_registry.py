"""ResearchDB Directory Registry — standard paths and structure validation."""
from __future__ import annotations
from pathlib import Path

RESEARCH_DB_ROOT = Path("data/research_db")

SUB_DIRECTORIES = [
    "account",
    "universe",
    "market",
    "finance",
    "signal",
    "outcome",
    "factor",
    "event",
    "caseforge",
    "knowledge",
]

KNOWLEDGE_SUB_DIRS = [
    "methodology",
    "industries",
    "chains",
    "company_profiles",
    "false_signal_library",
]


def get_directory_registry() -> dict[str, Path]:
    """Return mapping of directory names to paths."""
    return {d: RESEARCH_DB_ROOT / d for d in SUB_DIRECTORIES}


def validate_directory_structure(root: Path | None = None) -> dict:
    """Validate that all standard ResearchDB directories exist.

    Args:
        root: Override root path. Defaults to RESEARCH_DB_ROOT.

    Returns:
        dict with status, existing, and missing directories.
    """
    root = root or RESEARCH_DB_ROOT
    existing = []
    missing = []
    for d in SUB_DIRECTORIES:
        p = root / d
        if p.exists() and p.is_dir():
            existing.append(d)
        else:
            missing.append(d)
    return {
        "status": "PASS" if not missing else "PARTIAL",
        "existing": existing,
        "missing": missing,
        "root": str(root),
    }
