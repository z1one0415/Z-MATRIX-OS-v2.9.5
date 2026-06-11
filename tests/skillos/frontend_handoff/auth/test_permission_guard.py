#!/usr/bin/env python3
"""test_permission_guard.py — Verify permission_guard.py works correctly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "skillos" / "frontend_handoff" / "auth"))

from permission_guard import (
    check_permission,
    get_role_permissions,
    list_roles,
    list_permissions,
    list_dangerous_permissions,
)


class TestCheckPermission:
    """Unit tests for check_permission function."""

    def test_valid_role_valid_permission_true(self):
        assert check_permission("admin", "can_view_dashboard") is True

    def test_valid_role_valid_permission_false(self):
        assert check_permission("viewer", "can_acknowledge_risk") is False

    def test_invalid_role_returns_false(self):
        assert check_permission("superadmin", "can_view_dashboard") is False

    def test_invalid_permission_returns_false(self):
        assert check_permission("admin", "can_format_universe") is False

    def test_empty_role_returns_false(self):
        assert check_permission("", "can_view_dashboard") is False

    def test_empty_permission_returns_false(self):
        assert check_permission("admin", "") is False

    def test_case_sensitivity(self):
        """Roles and permissions are case-sensitive."""
        assert check_permission("Admin", "can_view_dashboard") is False
        assert check_permission("ADMIN", "can_view_dashboard") is False

    def test_all_dangerous_false_across_all_roles(self):
        """Verify dangerous permissions are false for every role."""
        dang = list_dangerous_permissions()
        roles = list_roles()
        for role in roles:
            for perm in dang:
                assert check_permission(role, perm) is False, f"{role}.{perm}"


class TestGetRolePermissions:
    """Unit tests for get_role_permissions function."""

    def test_admin_has_15_permissions(self):
        perms = get_role_permissions("admin")
        assert len(perms) == 15, f"Expected 15 permissions, got {len(perms)}"

    def test_viewer_has_6_true(self):
        perms = get_role_permissions("viewer")
        true_count = sum(1 for v in perms.values() if v is True)
        assert true_count == 6, f"Viewer should have 6 true perms, got {true_count}"

    def test_analyst_has_7_true(self):
        perms = get_role_permissions("analyst")
        true_count = sum(1 for v in perms.values() if v is True)
        assert true_count == 7, f"Analyst should have 7 true perms, got {true_count}"

    def test_reviewer_has_9_true(self):
        perms = get_role_permissions("reviewer")
        true_count = sum(1 for v in perms.values() if v is True)
        assert true_count == 9, f"Reviewer should have 9 true perms, got {true_count}"

    def test_approver_has_10_true(self):
        perms = get_role_permissions("approver")
        true_count = sum(1 for v in perms.values() if v is True)
        assert true_count == 10, f"Approver should have 10 true perms, got {true_count}"

    def test_admin_has_10_true(self):
        """Admin: all non-dangerous = true (10), dangerous = false (5)."""
        perms = get_role_permissions("admin")
        true_count = sum(1 for v in perms.values() if v is True)
        assert true_count == 10, f"Admin should have 10 true perms, got {true_count}"

    def test_system_auditor_has_6_true(self):
        perms = get_role_permissions("system_auditor")
        true_count = sum(1 for v in perms.values() if v is True)
        assert true_count == 6, f"System auditor should have 6 true perms, got {true_count}"

    def test_unknown_role_returns_empty(self):
        assert get_role_permissions("ghost") == {}


class TestListFunctions:
    """Unit tests for list helper functions."""

    def test_list_roles_returns_6(self):
        roles = list_roles()
        assert len(roles) == 6

    def test_list_roles_contains_all_expected(self):
        roles = list_roles()
        expected = {"viewer", "analyst", "reviewer", "approver", "admin", "system_auditor"}
        assert set(roles) == expected

    def test_list_permissions_returns_15(self):
        perms = list_permissions()
        assert len(perms) == 15

    def test_list_dangerous_permissions_returns_5(self):
        dang = list_dangerous_permissions()
        assert len(dang) == 5
        expected = {
            "can_enable_runtime",
            "can_enable_runner",
            "can_enable_paper_trading",
            "can_enable_broker",
            "can_enable_production",
        }
        assert set(dang) == expected


class TestProgressiveTrustInheritance:
    """Verify the strict inheritance chain: viewer ⊂ analyst ⊂ reviewer ⊂ approver ⊂ admin."""

    def test_analyst_superset_of_viewer(self):
        viewer = get_role_permissions("viewer")
        analyst = get_role_permissions("analyst")
        for perm, val in viewer.items():
            if val is True:
                assert analyst[perm] is True, f"analyst should inherit viewer.{perm}"

    def test_reviewer_superset_of_analyst(self):
        analyst = get_role_permissions("analyst")
        reviewer = get_role_permissions("reviewer")
        for perm, val in analyst.items():
            if val is True:
                assert reviewer[perm] is True, f"reviewer should inherit analyst.{perm}"

    def test_approver_superset_of_reviewer(self):
        reviewer = get_role_permissions("reviewer")
        approver = get_role_permissions("approver")
        for perm, val in reviewer.items():
            if val is True:
                assert approver[perm] is True, f"approver should inherit reviewer.{perm}"

    def test_admin_superset_of_approver(self):
        approver = get_role_permissions("approver")
        admin = get_role_permissions("admin")
        for perm, val in approver.items():
            if val is True:
                assert admin[perm] is True, f"admin should inherit approver.{perm}"
