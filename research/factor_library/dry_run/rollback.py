"""
Rollback — No-cleanup rollback plan.

Since no execution ever occurs in disabled-default, no cleanup
is ever required. This module provides a static rollback plan
that always reports cleanup_required=False.
"""

from __future__ import annotations


def rollback_plan() -> dict:
    """
    Return a rollback plan for the noop dry-run.

    In disabled-default, no execution occurs, so no cleanup
    is ever required. All cleanup flags are hard-coded False.

    Returns:
        A dict with all cleanup flags set to False.
    """
    return {
        "cleanup_required": False,
        "runtime_report_cleanup_required": False,
        "runtime_audit_cleanup_required": False,
        "factor_result_cleanup_required": False,
        "reason": "no execution occurred",
    }
