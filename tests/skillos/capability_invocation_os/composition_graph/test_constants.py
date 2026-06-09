"""Tests for composition_graph.constants."""
from skillos.capability_invocation_os.composition_graph.constants import (
    GRAPH_MODE, ALLOWED_NODE_TYPES, BLOCKED_NODE_TYPES,
    ALLOWED_EDGE_TYPES, BLOCKED_EDGE_TYPES, FORBIDDEN_GRAPH_OUTPUTS,
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
    from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.constants import FORBIDDEN_BRIDGE_OUTPUTS
    assert FORBIDDEN_GRAPH_OUTPUTS == FORBIDDEN_BRIDGE_OUTPUTS

def test_no_overlap_allowed_blocked_nodes():
    assert ALLOWED_NODE_TYPES.isdisjoint(BLOCKED_NODE_TYPES)

def test_no_overlap_allowed_blocked_edges():
    assert ALLOWED_EDGE_TYPES.isdisjoint(BLOCKED_EDGE_TYPES)

def test_allowed_node_types_canonical_names():
    expected = frozenset({"static_input_node","capability_registry_node","a1_factor_bridge_response_node","a1_factor_bridge_denied_context_node","factor_evidence_summary_node","local_report_reading_node","document_generation_in_memory_node","composition_summary_node"})
    assert ALLOWED_NODE_TYPES == expected

def test_blocked_node_types_canonical_names():
    required = {"factor_library_direct_node","real_factor_node","z2_runtime_node","z8_execution_node","z9_memory_mutation_node","v3_sandbox_node","broker_node","real_trade_node","alpha_signal_node","paper_trading_node","portfolio_weight_node","order_signal_node","production_node"}
    assert required.issubset(BLOCKED_NODE_TYPES)

def test_allowed_edge_types_canonical_names():
    expected = frozenset({"readonly_context_edge","evidence_hash_edge","permission_tier_edge","degradation_edge","denied_context_edge","blocked_output_filter_edge","c1_handoff_edge","a1_bridge_source_edge"})
    assert ALLOWED_EDGE_TYPES == expected

def test_blocked_edge_types_canonical_names():
    required = {"execution_edge","trade_edge","broker_edge","real_time_feedback_edge","autonomous_retry_edge","mutation_edge","production_edge","alpha_signal_edge"}
    assert required.issubset(BLOCKED_EDGE_TYPES)
