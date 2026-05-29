"""V4.0-C3 Research Council — Reviewer Registry

Provides dynamic loading of all 12 independent reviewer modules
from the reviewers/ package directory.
"""
from __future__ import annotations
import importlib, pkgutil
from pathlib import Path


def get_registry() -> dict:
    """Load all independent reviewer modules and return a registry dict.

    Returns:
        dict mapping reviewer_id (str) to module's review function.
        Each review function signature: review(facts: dict | None = None) -> ReviewerOutput.
    """
    import zmatrix.research_council.reviewers as pkg

    result = {}
    for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
        if not module_name.startswith("r") or len(module_name) < 5:
            continue
        # Skip infrastructure modules
        if module_name in ("r00_", "base_reviewer", "reviewer_registry", "council_aggregator", "scoring_config"):
            continue
        try:
            mod = importlib.import_module(f"zmatrix.research_council.reviewers.{module_name}")
            if hasattr(mod, "REVIEWER_CONFIG") and hasattr(mod, "review"):
                rid = mod.REVIEWER_CONFIG.get("reviewer_id", module_name.upper())
                result[rid] = mod.review
        except ImportError:
            continue
    return result


def count_reviewers() -> int:
    """Return count of loaded independent reviewers."""
    return len(get_registry())


def list_reviewer_ids() -> list[str]:
    """Return sorted list of all reviewer IDs."""
    return sorted(get_registry().keys())
