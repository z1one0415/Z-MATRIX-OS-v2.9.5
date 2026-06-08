"""Proof: permissions — write/production/broker/real_trade all denied."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.permissions import (
    validate_wave0_execution_permission, Wave0ExecutionPermission,
    check_permission, ALWAYS_DENIED,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_write_denied():
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.GITHUB_READONLY, Wave0ExecutionPermission.WRITE
    ) is False


def test_production_denied():
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.GITHUB_READONLY, Wave0ExecutionPermission.PRODUCTION
    ) is False


def test_broker_denied():
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.GITHUB_READONLY, Wave0ExecutionPermission.BROKER
    ) is False


def test_real_trade_denied():
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.GITHUB_READONLY, Wave0ExecutionPermission.REAL_TRADE
    ) is False


def test_file_write_denied():
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.REPORT_READING, Wave0ExecutionPermission.FILE_WRITE
    ) is False


def test_network_denied():
    """P0: network permission denied."""
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.GITHUB_READONLY, Wave0ExecutionPermission.NETWORK
    ) is False


def test_unknown_permission_denied():
    assert validate_wave0_execution_permission(
        Wave0AdapterKind.GITHUB_READONLY, "NOT_A_PERMISSION"
    ) is False


def test_always_denied_set():
    for perm in ALWAYS_DENIED:
        for kind in Wave0AdapterKind:
            assert validate_wave0_execution_permission(kind, perm) is False


def test_check_permission_always_denies():
    assert check_permission(None) is False
    assert check_permission("READ_ONLY") is False
    assert check_permission(True) is False
