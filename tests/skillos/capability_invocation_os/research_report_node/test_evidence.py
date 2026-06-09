"""Tests for Research Report Node evidence building."""

from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphResponse,
    CompositionGraphDecision,
    CompositionGraphEvidence,
)
from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportEvidence,
    ResearchReportSection,
)
from skillos.capability_invocation_os.research_report_node.evidence import (
    build_report_evidence_from_b1_graph,
    build_z2_report_node_hash,
    build_z2_report_section_hash,
    build_z2_report_evidence_hash,
    build_report_evidence_refs,
)


def _make_b1_evidence():
    return CompositionGraphEvidence(
        source_class="factor_library_fixture",
        no_real_source_flag=True,
        fixture_source_commit="P1_FIXTURE_ONLY",
        graph_node_hash="node_h",
        graph_edge_hash="edge_h",
        permission_tier="T0",
        forbidden_outputs_removed_hash="frh",
        rollback_marker=False,
        privacy_marker=True,
        c1_handoff_marker=True,
    )


def _make_b1_response():
    return CompositionGraphResponse(
        response_id="b1-ev-test",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence=_make_b1_evidence(),
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        graph_enabled=False,
        execution_enabled=False,
    )


def test_build_report_evidence_from_b1_graph_returns_evidence():
    """build_report_evidence_from_b1_graph returns ResearchReportEvidence."""
    ev = build_report_evidence_from_b1_graph(_make_b1_response(), "resp-1")
    assert isinstance(ev, ResearchReportEvidence)


def test_build_report_evidence_inherits_source_class():
    """Evidence inherits source_class from B1."""
    ev = build_report_evidence_from_b1_graph(_make_b1_response(), "resp-2")
    assert ev.source_class == "factor_library_fixture"


def test_build_report_evidence_inherits_no_real_source_flag():
    """Evidence inherits no_real_source_flag."""
    ev = build_report_evidence_from_b1_graph(_make_b1_response(), "resp-3")
    assert ev.no_real_source_flag is True


def test_build_report_evidence_has_report_node_hash():
    """Evidence has non-empty z2_report_node_hash."""
    ev = build_report_evidence_from_b1_graph(_make_b1_response(), "resp-4")
    assert ev.z2_report_node_hash != ""


def test_build_report_evidence_has_evidence_hash():
    """Evidence has non-empty z2_report_evidence_hash."""
    ev = build_report_evidence_from_b1_graph(_make_b1_response(), "resp-5")
    assert ev.z2_report_evidence_hash != ""


def test_build_report_evidence_from_dict_evidence():
    """Build evidence from B1 with dict evidence."""
    resp = CompositionGraphResponse(
        response_id="dict-ev",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={"source_class": "fixture", "no_real_source_flag": True, "fixture_source_commit": "X"},
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-6")
    assert ev.source_class == "fixture"


def test_build_z2_report_node_hash_deterministic():
    """Same inputs produce same hash."""
    h1 = build_z2_report_node_hash("id1", "DISABLED_DEFAULT_P0")
    h2 = build_z2_report_node_hash("id1", "DISABLED_DEFAULT_P0")
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 hex


def test_build_z2_report_section_hash_deterministic():
    """Same inputs produce same hash."""
    h1 = build_z2_report_section_hash("sec1", "report_header")
    h2 = build_z2_report_section_hash("sec1", "report_header")
    assert h1 == h2


def test_build_z2_report_evidence_hash_deterministic():
    """Same evidence produces same hash."""
    ev = ResearchReportEvidence(source_class="test", permission_tier="T0")
    h1 = build_z2_report_evidence_hash(ev)
    h2 = build_z2_report_evidence_hash(ev)
    assert h1 == h2


def test_build_report_evidence_refs():
    """build_report_evidence_refs returns list of hashes."""
    sections = [
        ResearchReportSection(section_id="s1", section_type="report_header"),
        ResearchReportSection(section_id="s2", section_type="risk_warning"),
    ]
    refs = build_report_evidence_refs(sections)
    assert len(refs) == 2
    assert all(isinstance(r, str) and len(r) == 64 for r in refs)



def test_build_report_evidence_inherits_request_hash():
    """Evidence inherits request_hash from B1 evidence dict."""
    resp = CompositionGraphResponse(
        response_id="rh-test",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={
            "source_class": "fixture",
            "no_real_source_flag": True,
            "fixture_source_commit": "X",
            "request_hash": "req_from_b1",
            "response_hash_placeholder": "resp_from_b1",
            "factor_decision_hash": "fdh",
            "bridge_decision_hash": "bdh",
            "graph_node_hash": "gnh",
            "graph_edge_hash": "geh",
        },
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-rh")
    assert ev.request_hash == "req_from_b1"


def test_build_report_evidence_inherits_response_hash_placeholder():
    """Evidence inherits response_hash_placeholder from B1 evidence dict."""
    resp = CompositionGraphResponse(
        response_id="rhp-test",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={
            "source_class": "fixture",
            "no_real_source_flag": True,
            "response_hash_placeholder": "resp_placeholder_inherited",
            "request_hash": "rh",
            "factor_decision_hash": "fdh",
            "bridge_decision_hash": "bdh",
            "graph_node_hash": "gnh",
            "graph_edge_hash": "geh",
        },
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-rhp")
    assert ev.response_hash_placeholder == "resp_placeholder_inherited"


def test_build_report_evidence_inherits_factor_decision_hash():
    """Evidence inherits factor_decision_hash from B1 evidence dict."""
    resp = CompositionGraphResponse(
        response_id="fdh-test",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={
            "source_class": "fixture",
            "no_real_source_flag": True,
            "request_hash": "rh",
            "response_hash_placeholder": "rhp",
            "factor_decision_hash": "factor_inherited_123",
            "bridge_decision_hash": "bdh",
            "graph_node_hash": "gnh",
            "graph_edge_hash": "geh",
        },
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-fdh")
    assert ev.factor_decision_hash == "factor_inherited_123"


def test_build_report_evidence_inherits_bridge_decision_hash():
    """Evidence inherits bridge_decision_hash from B1 evidence dict."""
    resp = CompositionGraphResponse(
        response_id="bdh-test",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={
            "source_class": "fixture",
            "no_real_source_flag": True,
            "request_hash": "rh",
            "response_hash_placeholder": "rhp",
            "factor_decision_hash": "fdh",
            "bridge_decision_hash": "bridge_inherited_456",
            "graph_node_hash": "gnh",
            "graph_edge_hash": "geh",
        },
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-bdh")
    assert ev.bridge_decision_hash == "bridge_inherited_456"


def test_build_report_evidence_missing_factor_decision_hash_computed():
    """factor_decision_hash is computed (non-empty) when not in B1 evidence."""
    resp = CompositionGraphResponse(
        response_id="fdh-missing",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={
            "source_class": "fixture",
            "no_real_source_flag": True,
            "graph_node_hash": "gnh",
            "graph_edge_hash": "geh",
        },
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-fdh-m")
    assert ev.factor_decision_hash != ""
    assert len(ev.factor_decision_hash) == 64


def test_build_report_evidence_missing_bridge_decision_hash_computed():
    """bridge_decision_hash is computed (non-empty) when not in B1 evidence."""
    resp = CompositionGraphResponse(
        response_id="bdh-missing",
        decision=CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY,
        evidence={
            "source_class": "fixture",
            "no_real_source_flag": True,
            "graph_node_hash": "gnh",
            "graph_edge_hash": "geh",
        },
        forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
    )
    ev = build_report_evidence_from_b1_graph(resp, "resp-bdh-m")
    assert ev.bridge_decision_hash != ""
    assert len(ev.bridge_decision_hash) == 64
