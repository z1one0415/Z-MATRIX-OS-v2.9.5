"""Tests for composition_graph.graph — CompositionGraphFactorBridge."""
from unittest.mock import patch
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse, A1FactorBridgeDecision, A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.graph import CompositionGraphFactorBridge
from skillos.capability_invocation_os.composition_graph.models import CompositionGraphDecision, CompositionGraphResponse

def _make_valid_response():
    return A1FactorBridgeResponse(response_id="test-123",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True),forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)

def _make_denied_response():
    return A1FactorBridgeResponse(response_id="test-denied",decision=A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED,evidence=A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True),forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=True,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)

def test_default_returns_disabled_noop():
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_valid_response())
    assert isinstance(result, CompositionGraphResponse)
    assert result.decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP
    assert result.degraded is True

def test_none_response_returns_disabled_noop():
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    assert bridge.process(None).decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_valid_response_allows_readonly(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_valid_response())
    assert result.decision == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY
    assert result.degraded is False
    assert len(result.nodes) == 2
    assert len(result.edges) == 2

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_denied_bridge_response(mock_config, mock_kill):
    result = CompositionGraphFactorBridge(fixture_mode=True).process(_make_denied_response())
    assert result.decision == CompositionGraphDecision.DENY_GRAPH_BRIDGE_DENIED
    assert result.degraded is True

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_invalid_type_denies_source(mock_config, mock_kill):
    assert CompositionGraphFactorBridge(fixture_mode=True).process({"not": "valid"}).decision == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_outputs_unsafe(mock_config, mock_kill):
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True),forbidden_outputs_removed=["alpha_claim"],degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert CompositionGraphFactorBridge(fixture_mode=True).process(resp).decision == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_not_fixture_mode_returns_disabled(mock_config, mock_kill):
    assert CompositionGraphFactorBridge(fixture_mode=False).process(_make_valid_response()).decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_response_has_forbidden_outputs_removed(mock_config, mock_kill):
    result = CompositionGraphFactorBridge(fixture_mode=True).process(_make_valid_response())
    assert set(result.forbidden_outputs_removed) == FORBIDDEN_GRAPH_OUTPUTS

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_response_id_prefixed(mock_config, mock_kill):
    assert CompositionGraphFactorBridge(fixture_mode=True).process(_make_valid_response()).response_id.startswith("graph_")

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_allowed_graph_nodes_have_canonical_types(mock_config, mock_kill):
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_NODE_TYPES
    result = CompositionGraphFactorBridge(fixture_mode=True).process(_make_valid_response())
    for node in result.nodes:
        assert node.node_type in ALLOWED_NODE_TYPES

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_allowed_graph_edges_have_canonical_types(mock_config, mock_kill):
    from skillos.capability_invocation_os.composition_graph.constants import ALLOWED_EDGE_TYPES
    result = CompositionGraphFactorBridge(fixture_mode=True).process(_make_valid_response())
    for edge in result.edges:
        assert edge.edge_type in ALLOWED_EDGE_TYPES

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_denied_graph_has_no_summary_node(mock_config, mock_kill):
    result = CompositionGraphFactorBridge(fixture_mode=True).process(_make_denied_response())
    for node in result.nodes:
        assert node.node_type != "composition_summary_node"

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_payload_forbidden_leak_denied(mock_config, mock_kill):
    from skillos.capability_invocation_os.composition_graph.contracts import validate_graph_payload_no_forbidden_outputs
    assert validate_graph_payload_no_forbidden_outputs({"alpha_claim": 0.05}) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_dag_validation_runs_on_allow_path(mock_config, mock_kill):
    assert CompositionGraphFactorBridge(fixture_mode=True).process(_make_valid_response()).decision == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY

@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
@patch("skillos.capability_invocation_os.composition_graph.graph.validate_dag_integrity", return_value=False)
def test_dag_invalid_returns_deny(mock_dag, mock_config, mock_kill):
    result = CompositionGraphFactorBridge(fixture_mode=True).process(_make_valid_response())
    assert result.decision == CompositionGraphDecision.DENY_GRAPH_DAG_INVALID
    assert result.degraded is True
