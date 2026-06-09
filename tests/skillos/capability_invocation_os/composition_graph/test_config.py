"""Tests for composition_graph.config."""

from skillos.capability_invocation_os.composition_graph.config import (
    is_composition_graph_enabled,
    is_graph_execution_enabled,
    is_graph_mutable_state_enabled,
    is_graph_real_source_enabled,
    is_graph_production_enabled,
    is_graph_alpha_enabled,
    is_graph_signal_enabled,
)


def test_composition_graph_disabled():
    assert is_composition_graph_enabled() is False


def test_graph_execution_disabled():
    assert is_graph_execution_enabled() is False


def test_graph_mutable_state_disabled():
    assert is_graph_mutable_state_enabled() is False


def test_graph_real_source_disabled():
    assert is_graph_real_source_enabled() is False


def test_graph_production_disabled():
    assert is_graph_production_enabled() is False


def test_graph_alpha_disabled():
    assert is_graph_alpha_enabled() is False


def test_graph_signal_disabled():
    assert is_graph_signal_enabled() is False
