"""Tests for composition_graph.config."""
from skillos.capability_invocation_os.composition_graph.config import is_composition_graph_enabled, set_composition_graph_enabled

def test_default_disabled():
    assert is_composition_graph_enabled() is False

def test_set_enabled():
    set_composition_graph_enabled(True)
    assert is_composition_graph_enabled() is True
    set_composition_graph_enabled(False)

def test_set_disabled():
    set_composition_graph_enabled(False)
    assert is_composition_graph_enabled() is False
