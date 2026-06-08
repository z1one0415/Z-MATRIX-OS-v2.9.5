"""Proof: kill switch — all active, overrides config."""
import pytest
from skillos.capability_invocation_os.adapters.wave0.kill_switch import (
    Wave0KillSwitch, get_kill_switch, reset_kill_switch,
)
from skillos.capability_invocation_os.adapters.wave0.models import Wave0AdapterKind


def test_kill_switch_default_all_active():
    ks = Wave0KillSwitch()
    assert ks.master is True
    assert ks.github is True
    assert ks.is_any_active() is True
    assert ks.is_master_active() is True


def test_master_kill_overrides_all():
    ks = Wave0KillSwitch(master=True)
    assert ks.is_adapter_killed(Wave0AdapterKind.GITHUB_READONLY) is True
    assert ks.is_adapter_killed(Wave0AdapterKind.DOCUMENT_GENERATION) is True
    assert ks.is_adapter_killed(Wave0AdapterKind.REPORT_READING) is True


def test_per_adapter_kill():
    """Per-adapter kill: master=False, github=True, docgen=False."""
    ks = Wave0KillSwitch(master=False, github=True, docgen=False)
    assert ks.is_adapter_killed(Wave0AdapterKind.GITHUB_READONLY) is True
    # docgen=False → per-adapter kill not active for docgen, but P0 execution still disabled
    assert ks.is_adapter_killed(Wave0AdapterKind.DOCUMENT_GENERATION) is False


def test_evidence_kill_blocks_sink():
    ks = Wave0KillSwitch(evidence=True)
    assert ks.is_evidence_killed() is True


def test_output_kill_blocks_generation():
    ks = Wave0KillSwitch(output=True)
    assert ks.is_output_killed() is True


def test_global_singleton():
    ks = get_kill_switch()
    assert ks.master is True
    reset_kill_switch()
    assert ks.master is True


def test_unknown_adapter_killed():
    """Unknown adapter = killed by default."""
    ks = Wave0KillSwitch(master=False, github=False)
    # Use a string that's not a Wave0AdapterKind
    assert ks.is_adapter_killed("UNKNOWN") is True
