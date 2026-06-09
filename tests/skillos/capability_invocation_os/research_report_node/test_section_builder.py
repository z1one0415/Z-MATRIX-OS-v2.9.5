"""Tests for Research Report Node section builders."""

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
    ALLOWED_REPORT_SECTIONS,
)
from skillos.capability_invocation_os.research_report_node.section_builder import (
    build_report_header_section,
    build_source_graph_summary_section,
    build_factor_context_summary_section,
    build_evidence_chain_summary_section,
    build_structural_readiness_summary_section,
    build_research_interpretation_section,
    build_risk_warning_section,
    build_missing_evidence_section,
    build_blocked_outputs_removed_section,
    build_confidence_section,
    build_next_validation_requirement_section,
)


def test_report_header_section():
    """build_report_header_section produces valid section."""
    s = build_report_header_section()
    assert s.section_type == "report_header"
    assert s.readonly_only is True
    assert s.no_alpha_claim is True
    assert s.section_id != ""


def test_source_graph_summary_section():
    """build_source_graph_summary_section produces valid section."""
    s = build_source_graph_summary_section(source_refs=["ref1"])
    assert s.section_type == "source_graph_summary"
    assert s.source_refs == ["ref1"]
    assert s.readonly_only is True


def test_factor_context_summary_section():
    """build_factor_context_summary_section produces MEDIUM confidence."""
    s = build_factor_context_summary_section()
    assert s.section_type == "factor_context_summary"
    assert s.confidence_level == "MEDIUM"


def test_structural_readiness_summary_section():
    """build_structural_readiness_summary_section produces HIGH_WITH_STRUCTURE_ONLY."""
    s = build_structural_readiness_summary_section()
    assert s.section_type == "structural_readiness_summary"
    assert s.confidence_level == "HIGH_WITH_STRUCTURE_ONLY"


def test_all_sections_have_forbidden_outputs_removed():
    """All section builders include forbidden_outputs_removed."""
    builders = [
        build_report_header_section,
        build_source_graph_summary_section,
        build_factor_context_summary_section,
        build_evidence_chain_summary_section,
        build_structural_readiness_summary_section,
        build_research_interpretation_section,
        build_risk_warning_section,
        build_missing_evidence_section,
        build_blocked_outputs_removed_section,
        build_confidence_section,
        build_next_validation_requirement_section,
    ]
    for builder in builders:
        section = builder()
        assert set(section.blocked_outputs_removed) == FORBIDDEN_REPORT_OUTPUTS


def test_all_sections_have_valid_section_types():
    """All section builders produce allowed section types."""
    builders = [
        build_report_header_section,
        build_source_graph_summary_section,
        build_factor_context_summary_section,
        build_evidence_chain_summary_section,
        build_structural_readiness_summary_section,
        build_research_interpretation_section,
        build_risk_warning_section,
        build_missing_evidence_section,
        build_blocked_outputs_removed_section,
        build_confidence_section,
        build_next_validation_requirement_section,
    ]
    for builder in builders:
        section = builder()
        assert section.section_type in ALLOWED_REPORT_SECTIONS


def test_confidence_section_with_invalid_level_defaults_low():
    """build_confidence_section with invalid level defaults to LOW."""
    s = build_confidence_section(confidence_level="INVALID")
    assert s.confidence_level == "LOW"


def test_missing_evidence_section_tracks_refs():
    """build_missing_evidence_section stores missing refs."""
    s = build_missing_evidence_section(missing=["ref_a", "ref_b"])
    assert s.evidence_refs == ["ref_a", "ref_b"]
    assert s.degradation_status == "missing"
