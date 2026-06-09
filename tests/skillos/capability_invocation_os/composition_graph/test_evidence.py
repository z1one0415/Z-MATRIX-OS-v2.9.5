"""Tests for composition_graph.evidence."""

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeDecision,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.evidence import (
    build_graph_node_hash,
    build_graph_edge_hash,
    build_graph_evidence_from_a1_response,
    build_graph_c1_handoff,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphEvidence,
)


def _make_response():
    return A1FactorBridgeResponse(
        response_id="test-ev",
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,
        evidence=A1FactorBridgeEvidence(
            source_commit="P1_FIXTURE_ONLY",
            source_class="factor_library_fixture",
            no_real_source_flag=True,
            fixture_source_commit="P1_FIXTURE_ONLY",
            request_hash="req_h",
            response_hash_placeholder="resp_h",
            factor_decision_hash="factor_h",
            bridge_decision_hash="bridge_h",
            permission_tier="T0",
            forbidden_outputs_removed_hash="forb_h",
            rollback_marker=False,
            privacy_marker=True,
            c1_handoff_marker=True,
        ),
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        bridge_enabled=False,
        runtime_enabled=False,
        adapter_execution_enabled=False,
        capability_execution_enabled=False,
    )


def test_node_hash_deterministic():
    h1 = build_graph_node_hash("n1", "type_a", "payload")
    h2 = build_graph_node_hash("n1", "type_a", "payload")
    assert h1 == h2
    assert len(h1) == 16


def test_edge_hash_deterministic():
    h1 = build_graph_edge_hash("e1", "type_a", "src", "tgt")
    h2 = build_graph_edge_hash("e1", "type_a", "src", "tgt")
    assert h1 == h2
    assert len(h1) == 16


def test_evidence_from_a1_response():
    ev = build_graph_evidence_from_a1_response(_make_response())
    assert isinstance(ev, CompositionGraphEvidence)
    assert ev.source_class == "factor_library_fixture"
    assert ev.no_real_source_flag is True
    assert ev.permission_tier == "T0"
    assert ev.c1_handoff_marker is True


def test_evidence_a1_hash_populated():
    ev = build_graph_evidence_from_a1_response(_make_response())
    assert ev.a1_evidence_hash != ""
    assert len(ev.a1_evidence_hash) == 16


def test_c1_handoff_structure():
    ev = CompositionGraphEvidence(
        source_class="factor_library_fixture",
        permission_tier="T0",
        c1_handoff_marker=True,
    )
    handoff = build_graph_c1_handoff(ev)
    assert handoff["c1_handoff_marker"] is True
    assert handoff["source_class"] == "factor_library_fixture"
    assert handoff["permission_tier"] == "T0"
