#!/usr/bin/env python3
"""test_dangerous_permissions_default_false.py — ALL 5 dangerous permissions must be FALSE for ALL 6 roles."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "skillos" / "frontend_handoff" / "auth"))

from permission_guard import check_permission, list_roles, list_dangerous_permissions


DANGEROUS_PERMISSIONS = [
    "can_enable_runtime",
    "can_enable_runner",
    "can_enable_paper_trading",
    "can_enable_broker",
    "can_enable_production",
]


def test_all_dangerous_permissions_defined():
    """Verify exactly 5 dangerous permissions exist."""
    dang = list_dangerous_permissions()
    assert len(dang) == 5, f"Expected 5 dangerous permissions, got {len(dang)}: {dang}"
    assert set(dang) == set(DANGEROUS_PERMISSIONS)


def test_viewer_dangerous_all_false():
    """Viewer: all dangerous = FALSE."""
    for perm in DANGEROUS_PERMISSIONS:
        result = check_permission("viewer", perm)
        assert result is False, f"viewer.{perm} should be False, got {result}"


def test_analyst_dangerous_all_false():
    """Analyst: all dangerous = FALSE."""
    for perm in DANGEROUS_PERMISSIONS:
        result = check_permission("analyst", perm)
        assert result is False, f"analyst.{perm} should be False, got {result}"


def test_reviewer_dangerous_all_false():
    """Reviewer: all dangerous = FALSE."""
    for perm in DANGEROUS_PERMISSIONS:
        result = check_permission("reviewer", perm)
        assert result is False, f"reviewer.{perm} should be False, got {result}"


def test_approver_dangerous_all_false():
    """Approver: all dangerous = FALSE."""
    for perm in DANGEROUS_PERMISSIONS:
        result = check_permission("approver", perm)
        assert result is False, f"approver.{perm} should be False, got {result}"


def test_admin_dangerous_all_false():
    """Admin: all dangerous = FALSE — CRITICAL."""
    for perm in DANGEROUS_PERMISSIONS:
        result = check_permission("admin", perm)
        assert result is False, f"CRITICAL: admin.{perm} should be False, got {result}"


def test_system_auditor_dangerous_all_false():
    """System auditor: all dangerous = FALSE."""
    for perm in DANGEROUS_PERMISSIONS:
        result = check_permission("system_auditor", perm)
        assert result is False, f"system_auditor.{perm} should be False, got {result}"


def test_all_roles_all_dangerous_false():
    """Exhaustive: every role × every dangerous permission = FALSE."""
    roles = list_roles()
    assert len(roles) == 6, f"Expected 6 roles, got {len(roles)}"
    failures = []
    for role in roles:
        for perm in DANGEROUS_PERMISSIONS:
            result = check_permission(role, perm)
            if result is not False:
                failures.append(f"{role}.{perm} = {result} (expected False)")
    assert len(failures) == 0, "\n".join(failures)
