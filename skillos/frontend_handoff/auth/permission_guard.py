#!/usr/bin/env python3
"""
permission_guard.py — Z-SkillOS Frontend Handoff Auth Permission Guard

Loads role_permission_matrix.json and exposes check_permission(role, permission) -> bool.
All dangerous permissions default to FALSE for ALL roles.
"""

import json
from pathlib import Path
from typing import Dict

_MATRIX_PATH = Path(__file__).resolve().parent / "role_permission_matrix.json"

_permission_matrix: Dict[str, Dict[str, bool]] = {}
_ALL_PERMISSIONS: list = []
_ROLES: list = []


def _load_matrix() -> None:
    """Load and cache the role-permission matrix from disk."""
    global _permission_matrix, _ALL_PERMISSIONS, _ROLES
    with open(_MATRIX_PATH, "r") as f:
        data = json.load(f)
    _permission_matrix = data["matrix"]
    _ALL_PERMISSIONS = data["permissions"]
    _ROLES = data["roles"]


def check_permission(role: str, permission: str) -> bool:
    """
    Check whether the given role has the specified permission.

    Args:
        role: One of viewer, analyst, reviewer, approver, admin, system_auditor
        permission: One of the 16 defined permission keys

    Returns:
        True if the role has the permission, False otherwise.
        Unknown roles return False for all permissions.
        Unknown permissions return False for all roles.
    """
    if not _permission_matrix:
        _load_matrix()

    if role not in _permission_matrix:
        return False
    return _permission_matrix[role].get(permission, False)


def get_role_permissions(role: str) -> Dict[str, bool]:
    """
    Get the full permissions map for a role.

    Args:
        role: One of the 6 defined roles

    Returns:
        Dict of permission -> bool. Empty dict for unknown roles.
    """
    if not _permission_matrix:
        _load_matrix()

    return _permission_matrix.get(role, {})


def list_roles() -> list:
    """Return the list of valid role names."""
    if not _ROLES:
        _load_matrix()
    return list(_ROLES)


def list_permissions() -> list:
    """Return the list of valid permission names."""
    if not _ALL_PERMISSIONS:
        _load_matrix()
    return list(_ALL_PERMISSIONS)


def list_dangerous_permissions() -> list:
    """Return the list of dangerous permission names."""
    if not _permission_matrix:
        _load_matrix()
    with open(_MATRIX_PATH, "r") as f:
        data = json.load(f)
    return data.get("dangerous_permissions", [])
