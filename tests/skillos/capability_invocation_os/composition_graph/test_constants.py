"""Tests for composition_graph.constants."""

from skillos.capability_invocation_os.composition_graph.constants import (
    GRAPH_MODE,
    ALLOWED_NODE_TYPES,
    BLOCKED_NODE_TYPES,
    ALLOWED_EDGE_TYPES,
    BLOCKED_EDGE_TYPES,
    FORBIDDEN_GRAPH_OUTPUTS,
)


def test_graph_mode_value():
    assert GRAPH_MODE == "DISABLED_DEFAULT_P0"


def test_allowed_node_types_count():
    assert len(ALLOWED_NODE_TYPES) == 8


def test_blocked_node_types_count():
    assert len(BLOCKED_NODE_TYPES) == 13


def test_allowed_edge_types_count():
    assert len(ALLOWED_EDGE_TYPES) == 8


def test_blocked_edge_types_count():
    assert len(BLOCKED_EDGE_TYPES) == 8


def test_forbidden_graph_outputs_count():
    assert len(FORBIDDEN_GRAPH_OUTPUTS) == 9


def test_forbidden_graph_outputs_match_bridge():
    from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import (
        FORBIDDEN_BRIDGE_OUTPUTS,
    )
    assert FORBIDDEN_GRAPH_OUTPUTS == FORBIDDEN_BRIDGE_OUTPUTS


def test_no_overlap_allowed_blocked_nodes():
    assert ALLOWED_NODE_TYPES.isdisjoint(BLOCKED_NODE_TYPES)


def test_no_overlap_allowed_blocked_edges():
    assert ALLOWED_EDGE_TYPES.isdisjoint(BLOCKED_EDGE_TYPES)
