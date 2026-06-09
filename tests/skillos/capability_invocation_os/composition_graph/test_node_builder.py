"""Tests for composition_graph.node_builder."""
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse, A1FactorBridgeDecision, A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.node_builder import (
    build_a1_bridge_response_node, build_a1_bridge_denied_context_node,
    build_factor_evidence_summary_node, build_composition_summary_node,
    build_static_input_node, build_graph_evidence_node, build_graph_summary_node, build_graph_noop_node,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphNode, CompositionGraphEvidence, GraphSourceSummary,
)

def _make_response():
    return A1FactorBridgeResponse(
        response_id="test-node",
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,
        evidence=A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True),
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False,
    )

def test_build_bridge_response_node_type():
    node = build_a1_bridge_response_node(_make_response())
    assert isinstance(node, CompositionGraphNode)
    assert node.node_type == "a1_factor_bridge_response_node"

def test_build_bridge_response_node_has_id():
    assert build_a1_bridge_response_node(_make_response()).node_id.startswith("node_bridge_")

def test_build_bridge_response_node_has_hash():
    assert len(build_a1_bridge_response_node(_make_response()).hash_value) == 16

def test_build_bridge_response_node_valid():
    assert build_a1_bridge_response_node(_make_response()).valid is True

def test_build_denied_context_node():
    node = build_a1_bridge_denied_context_node(_make_response(), reason="test_reason")
    assert node.node_type == "a1_factor_bridge_denied_context_node"
    assert node.node_id.startswith("node_denied_")

def test_build_denied_context_node_valid_false():
    assert build_a1_bridge_denied_context_node(_make_response(), reason="x").valid is False

def test_build_factor_evidence_summary_node():
    node = build_factor_evidence_summary_node(CompositionGraphEvidence())
    assert node.node_type == "factor_evidence_summary_node"
    assert node.node_id.startswith("node_evidence_")

def test_build_composition_summary_node():
    node = build_composition_summary_node(GraphSourceSummary(source_class="test", total_nodes=1))
    assert node.node_type == "composition_summary_node"
    assert node.node_id.startswith("node_summary_")

def test_build_static_input_node():
    node = build_static_input_node()
    assert node.node_type == "static_input_node"
    assert node.node_id.startswith("node_static_")

def test_build_static_input_node_default_reason():
    assert build_static_input_node().payload["reason"] == "DISABLED_DEFAULT_P0"

def test_legacy_alias_graph_evidence_node():
    assert build_graph_evidence_node(CompositionGraphEvidence()).node_type == "factor_evidence_summary_node"

def test_legacy_alias_graph_summary_node():
    assert build_graph_summary_node(GraphSourceSummary()).node_type == "composition_summary_node"

def test_legacy_alias_graph_noop_node():
    assert build_graph_noop_node().node_type == "static_input_node"

def test_canonical_names_in_allowed():
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_NODE_TYPES
    assert build_a1_bridge_response_node(_make_response()).node_type in ALLOWED_NODE_TYPES

def test_denied_canonical_name_in_allowed():
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_NODE_TYPES
    assert build_a1_bridge_denied_context_node(_make_response(), reason="x").node_type in ALLOWED_NODE_TYPES

def test_evidence_canonical_name_in_allowed():
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_NODE_TYPES
    assert build_factor_evidence_summary_node(CompositionGraphEvidence()).node_type in ALLOWED_NODE_TYPES

def test_summary_canonical_name_in_allowed():
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_NODE_TYPES
    assert build_composition_summary_node(GraphSourceSummary()).node_type in ALLOWED_NODE_TYPES
