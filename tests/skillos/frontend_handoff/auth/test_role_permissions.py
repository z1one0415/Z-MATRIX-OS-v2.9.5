#!/usr/bin/env python3
"""test_role_permissions.py — Verify the role-permission matrix logic."""

import json
import sys
from pathlib import Path

# Add the auth module to path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "skillos" / "frontend_handoff" / "auth"))

from permission_guard import (
    check_permission,
    get_role_permissions,
    list_roles,
    list_permissions,
    list_dangerous_permissions,
)
import permission_guard as pg

MATRIX_PATH = (
    Path(__file__).resolve().parents[4]
    / "skillos"
    / "frontend_handoff"
    / "auth"
    / "role_permission_matrix.json"
)


def test_all_roles_present():
    """Verify exactly 6 roles are defined."""
    roles = list_roles()
    assert len(roles) == 6, f"Expected 6 roles, got {len(roles)}"
    expected = {"viewer", "analyst", "reviewer", "approver", "admin", "system_auditor"}
    assert set(roles) == expected, f"Missing roles: {expected - set(roles)}"


def test_all_permissions_present():
    """Verify all 15 permissions are defined (the spec says 16 but lists 15)."""
    perms = list_permissions()
    expected = {
        "can_view_dashboard",
        "can_view_factor_library",
        "can_view_reports",
        "can_view_reviews",
        "can_view_evidence_chain",
        "can_view_gate_state",
        "can_acknowledge_risk",
        "can_approve_planning_gate",
        "can_approve_interpretation_review",
        "can_approve_promotion_eligibility_review",
        "can_enable_runtime",
        "can_enable_runner",
        "can_enable_paper_trading",
        "can_enable_broker",
        "can_enable_production",
    }
    assert set(perms) == expected, f"Missing: {expected - set(perms)}, Extra: {set(perms) - expected}"


def test_viewer_permissions():
    """Viewer: view only, no other permissions."""
    assert check_permission("viewer", "can_view_dashboard") is True
    assert check_permission("viewer", "can_view_factor_library") is True
    assert check_permission("viewer", "can_view_reports") is True
    assert check_permission("viewer", "can_view_reviews") is True
    assert check_permission("viewer", "can_view_evidence_chain") is True
    assert check_permission("viewer", "can_view_gate_state") is True
    assert check_permission("viewer", "can_acknowledge_risk") is False
    assert check_permission("viewer", "can_approve_planning_gate") is False
    assert check_permission("viewer", "can_approve_interpretation_review") is False
    assert check_permission("viewer", "can_approve_promotion_eligibility_review") is False


def test_analyst_permissions():
    """Analyst: viewer + can_acknowledge_risk."""
    assert check_permission("analyst", "can_view_dashboard") is True
    assert check_permission("analyst", "can_acknowledge_risk") is True
    assert check_permission("analyst", "can_approve_planning_gate") is False
    assert check_permission("analyst", "can_approve_interpretation_review") is False
    assert check_permission("analyst", "can_approve_promotion_eligibility_review") is False


def test_reviewer_permissions():
    """Reviewer: analyst + approve planning gate + approve interpretation review."""
    assert check_permission("reviewer", "can_acknowledge_risk") is True
    assert check_permission("reviewer", "can_approve_planning_gate") is True
    assert check_permission("reviewer", "can_approve_interpretation_review") is True
    assert check_permission("reviewer", "can_approve_promotion_eligibility_review") is False


def test_approver_permissions():
    """Approver: reviewer + approve promotion eligibility review."""
    assert check_permission("approver", "can_approve_planning_gate") is True
    assert check_permission("approver", "can_approve_interpretation_review") is True
    assert check_permission("approver", "can_approve_promotion_eligibility_review") is True


def test_admin_permissions():
    """Admin: all non-dangerous permissions true; all dangerous false."""
    admin_perms = get_role_permissions("admin")
    non_dangerous = [
        "can_view_dashboard",
        "can_view_factor_library",
        "can_view_reports",
        "can_view_reviews",
        "can_view_evidence_chain",
        "can_view_gate_state",
        "can_acknowledge_risk",
        "can_approve_planning_gate",
        "can_approve_interpretation_review",
        "can_approve_promotion_eligibility_review",
    ]
    for p in non_dangerous:
        assert admin_perms[p] is True, f"admin should have {p} = True"


def test_system_auditor_permissions():
    """System auditor: view all only, no write/approve."""
    assert check_permission("system_auditor", "can_view_dashboard") is True
    assert check_permission("system_auditor", "can_view_factor_library") is True
    assert check_permission("system_auditor", "can_view_reports") is True
    assert check_permission("system_auditor", "can_view_reviews") is True
    assert check_permission("system_auditor", "can_view_evidence_chain") is True
    assert check_permission("system_auditor", "can_view_gate_state") is True
    assert check_permission("system_auditor", "can_acknowledge_risk") is False
    assert check_permission("system_auditor", "can_approve_planning_gate") is False
    assert check_permission("system_auditor", "can_approve_interpretation_review") is False
    assert check_permission("system_auditor", "can_approve_promotion_eligibility_review") is False


def test_unknown_role_returns_false():
    """Unknown roles return False for all permissions."""
    assert check_permission("superuser", "can_view_dashboard") is False
    assert check_permission("hacker", "can_enable_production") is False
    assert check_permission("", "can_view_dashboard") is False


def test_unknown_permission_returns_false():
    """Unknown permissions return False for all roles."""
    assert check_permission("admin", "can_delete_everything") is False
    assert check_permission("viewer", "can_hack_the_planet") is False


def test_dangerous_permissions_list():
    """Verify dangerous permissions list is correct."""
    dang = list_dangerous_permissions()
    expected = {
        "can_enable_runtime",
        "can_enable_runner",
        "can_enable_paper_trading",
        "can_enable_broker",
        "can_enable_production",
    }
    assert set(dang) == expected


def test_get_role_permissions_unknown():
    """get_role_permissions returns empty dict for unknown role."""
    assert get_role_permissions("nonexistent") == {}


def test_matrix_json_well_formed():
    """Verify the JSON file is well-formed and complete."""
    with open(MATRIX_PATH) as f:
        data = json.load(f)
    assert "matrix_version" in data
    assert len(data["roles"]) == 6
    assert len(data["permissions"]) == 15
    assert len(data["matrix"]) == 6
    for role in data["roles"]:
        assert role in data["matrix"], f"Role {role} missing from matrix"
        assert len(data["matrix"][role]) == 15, f"Role {role} has {len(data['matrix'][role])} perms, expected 15"
    assert data.get("all_dangerous_permissions_default_false") is True
