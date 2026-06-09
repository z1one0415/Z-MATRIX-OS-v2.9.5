"""Tests for composition_graph.kill_switch."""
from skillos.capability_invocation_os.composition_graph.kill_switch import should_force_disabled, set_force_disabled

def test_default_force_disabled():
    assert should_force_disabled() is True

def test_set_force_disabled_false():
    set_force_disabled(False)
    assert should_force_disabled() is False
    set_force_disabled(True)

def test_set_force_disabled_true():
    set_force_disabled(True)
    assert should_force_disabled() is True
