"""Path utilities for research factor tests."""
from pathlib import Path

def repo_root() -> Path:
    """Return repository root."""
    return Path(__file__).resolve().parent.parent

ROOT = repo_root()
CONFIG_FACTORS = ROOT / "configs" / "research" / "factors"
RUNTIME_FACTORS = ROOT / "runtime_reports" / "research" / "factors"
RUNTIME_AUDIT = ROOT / "runtime_reports" / "audit"
RUNTIME_CASES = ROOT / "runtime_reports" / "cases"
