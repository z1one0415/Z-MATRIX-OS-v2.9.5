"""Tests for composition_graph.evidence."""
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse, A1FactorBridgeDecision, A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.evidence import (
    build_graph_evidence_from_a1_response, build_graph_node_hash, build_graph_edge_hash, build_graph_c1_handoff,
)
from skillos.capability_invocation_os.composition_graph.models import CompositionGraphEvidence

def _make_response():
    return A1FactorBridgeResponse(response_id="test-ev",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence=A1FactorBridgeEvidence(source_commit="P1_FIXTURE_ONLY",source_class="factor_library_fixture",no_real_source_flag=True,fixture_source_commit="P1_FIXTURE_ONLY",request_hash="r",response_hash_placeholder="r",factor_decision_hash="f",bridge_decision_hash="b",permission_tier="T0",forbidden_outputs_removed_hash="h",rollback_marker=False,privacy_marker=True,c1_handoff_marker=True),forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)

def test_build_evidence_from_response():
    ev = build_graph_evidence_from_a1_response(_make_response())
    assert isinstance(ev, CompositionGraphEvidence)
    assert ev.source_class == "factor_library_fixture"
    assert ev.no_real_source_flag is True

def test_build_evidence_has_hash():
    assert len(build_graph_evidence_from_a1_response(_make_response()).a1_evidence_hash) == 16

def test_build_node_hash():
    assert len(build_graph_node_hash("node1", "type1", "payload")) == 16

def test_build_edge_hash():
    assert len(build_graph_edge_hash("edge1", "type1", "src", "tgt")) == 16

def test_c1_handoff():
    ev = CompositionGraphEvidence(c1_handoff_marker=True, source_class="test")
    handoff = build_graph_c1_handoff(ev)
    assert handoff["c1_handoff_marker"] is True
    assert handoff["source_class"] == "test"

def test_dict_evidence():
    resp = A1FactorBridgeResponse(response_id="d",decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,evidence={"source_class":"factor_library_fixture","no_real_source_flag":True},forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),degraded=False,mode="DISABLED_DEFAULT_P0",bridge_enabled=False,runtime_enabled=False,adapter_execution_enabled=False,capability_execution_enabled=False)
    ev = build_graph_evidence_from_a1_response(resp)
    assert ev.source_class == "factor_library_fixture"
