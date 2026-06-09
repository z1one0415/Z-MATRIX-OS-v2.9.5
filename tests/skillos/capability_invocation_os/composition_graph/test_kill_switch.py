"""Tests for composition_graph.kill_switch."""

from skillos.capability_invocation_os.composition_graph.kill_switch import (
    should_force_disabled,
    should_block_execution,
    should_block_mutable_state,
    should_block_real_source,
)


def test_force_disabled_active():
    assert should_force_disabled() is True


def test_block_execution_active():
    assert should_block_execution() is True


def test_block_mutable_state_active():
    assert should_block_mutable_state() is True


def test_block_real_source_active():
    assert should_block_real_source() is True
