"""Tests for composition_graph.contracts."""
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse, A1FactorBridgeDecision, A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.contracts import (
    validate_a1_bridge_response, validate_graph_node_type, validate_graph_edge_type,
    validate_no_blocked_nodes, validate_no_blocked_edges, validate_graph_payload_no_forbidden_outputs,
)
from skillos.capability_invocation_os.composition_graph.models import CompositionGraphDecision

def _make_valid_evidence():
    return A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True)

def _make_valid_response():
    return A1FactorBridgeResponse(response_id="test-123",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=_make_valid_evidence(),forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)

def test_validate_valid_response_allows():
    assert validate_a1_bridge_response(_make_valid_response()) == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY

def test_validate_not_a1_response_denies():
    assert validate_a1_bridge_response({"not": "a response"}) == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

def test_validate_none_response_denies():
    assert validate_a1_bridge_response(None) == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

def test_validate_none_evidence_denies():
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=None,forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert validate_a1_bridge_response(resp) == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

def test_validate_invalid_source_class_denies():
    ev = A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="INVALID",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True)
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=ev,forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert validate_a1_bridge_response(resp) == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN

def test_validate_no_real_source_false_denies():
    ev = A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=False,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True)
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=ev,forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert validate_a1_bridge_response(resp) == CompositionGraphDecision.DENY_GRAPH_REAL_SOURCE_FORBIDDEN

def test_validate_missing_forbidden_outputs_denies():
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=_make_valid_evidence(),forbidden_outputs_removed=["alpha_claim"],degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert validate_a1_bridge_response(resp) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

def test_validate_bridge_denied_decision():
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED,evidence=_make_valid_evidence(),forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=True,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert validate_a1_bridge_response(resp) == CompositionGraphDecision.DENY_GRAPH_BRIDGE_DENIED

def test_validate_dict_evidence_valid():
    resp = A1FactorBridgeResponse(response_id="t",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence={"source_class":"factor_library_disabled_default","no_real_source_flag":True},forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    assert validate_a1_bridge_response(resp) == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY

def test_validate_node_type_allowed():
    assert validate_graph_node_type("a1_factor_bridge_response_node") is True

def test_validate_node_type_blocked():
    assert validate_graph_node_type("factor_library_direct_node") is False

def test_validate_edge_type_allowed():
    assert validate_graph_edge_type("a1_bridge_source_edge") is True

def test_validate_edge_type_blocked():
    assert validate_graph_edge_type("execution_edge") is False

def test_no_blocked_nodes_pass():
    assert validate_no_blocked_nodes(["a1_factor_bridge_response_node", "static_input_node"]) is True

def test_no_blocked_nodes_fail():
    assert validate_no_blocked_nodes(["factor_library_direct_node"]) is False

def test_no_blocked_edges_pass():
    assert validate_no_blocked_edges(["a1_bridge_source_edge"]) is True

def test_no_blocked_edges_fail():
    assert validate_no_blocked_edges(["execution_edge"]) is False

# Payload scanning tests
def test_payload_alpha_claim_denied():
    assert validate_graph_payload_no_forbidden_outputs({"alpha_claim": 0.05}) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

def test_payload_position_weight_denied():
    assert validate_graph_payload_no_forbidden_outputs({"position_weight": 0.1}) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

def test_payload_nested_forbidden_denied():
    assert validate_graph_payload_no_forbidden_outputs({"inner": {"nested": {"alpha_claim": 0.05}}}) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

def test_payload_safe_allowed():
    assert validate_graph_payload_no_forbidden_outputs({"summary": "test"}) == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY

def test_payload_none_allowed():
    assert validate_graph_payload_no_forbidden_outputs(None) == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY

def test_payload_object_with_forbidden_attr():
    class FakePayload:
        def __init__(self):
            self.alpha_claim = 0.05
    assert validate_graph_payload_no_forbidden_outputs(FakePayload()) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

def test_payload_object_safe():
    class SafePayload:
        def __init__(self):
            self.summary = "ok"
    assert validate_graph_payload_no_forbidden_outputs(SafePayload()) == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY

def test_payload_buy_signal_denied():
    assert validate_graph_payload_no_forbidden_outputs({"buy_signal": True}) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE

def test_payload_order_signal_denied():
    assert validate_graph_payload_no_forbidden_outputs({"order_signal": {"ticker": "AAPL"}}) == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE
