"""Tests for Research Report Node models."""

from dataclasses import FrozenInstanceError

import pytest

from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    ResearchReportNodeRequest,
    ResearchReportNodeResponse,
    ResearchReportSection,
    ResearchReportEvidence,
    Z9ReviewSnapshotCandidate,
    ResearchReportSummary,
    ReportDegradationStatus,
)
from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)


def test_decision_enum_has_9_members():
    """ResearchReportDecision has exactly 9 members."""
    assert len(ResearchReportDecision) == 9


def test_request_defaults():
    """ResearchReportNodeRequest has correct defaults."""
    req = ResearchReportNodeRequest()
    assert req.request_id == ""
    assert req.intent == "Z2_READONLY_REPORT"
    assert req.execution_requested is False


def test_response_defaults():
    """ResearchReportNodeResponse has correct defaults."""
    resp = ResearchReportNodeResponse()
    assert resp.decision == ResearchReportDecision.DISABLED_DEFAULT_NOOP
    assert resp.degraded is True
    assert resp.mode == "DISABLED_DEFAULT_P0"
    assert resp.report_enabled is False
    assert resp.runtime_enabled is False
    assert resp.readonly_only is True
    assert resp.no_alpha_claim is True
    assert resp.no_trade_signal is True
    assert resp.no_position_weight is True


def test_response_forbidden_outputs_removed():
    """Response defaults include all FORBIDDEN_REPORT_OUTPUTS."""
    resp = ResearchReportNodeResponse()
    assert set(resp.forbidden_outputs_removed) == FORBIDDEN_REPORT_OUTPUTS


def test_section_defaults():
    """ResearchReportSection has correct defaults."""
    section = ResearchReportSection()
    assert section.section_id == ""
    assert section.confidence_level == "LOW"
    assert section.readonly_only is True
    assert section.no_alpha_claim is True
    assert section.no_trade_signal is True


def test_evidence_defaults():
    """ResearchReportEvidence has correct defaults."""
    ev = ResearchReportEvidence()
    assert ev.no_real_source_flag is True
    assert ev.permission_tier == "T0"
    assert ev.privacy_marker is True
    assert ev.c1_handoff_marker is True
    assert ev.rollback_marker is False


def test_z9_candidate_defaults():
    """Z9ReviewSnapshotCandidate has correct defaults."""
    z9 = Z9ReviewSnapshotCandidate()
    assert z9.readonly_only is True
    assert z9.no_trade_result is True
    assert z9.no_paper_trading is True
    assert z9.no_broker_action is True
    assert z9.no_position_change is True
    assert z9.confidence_level == "LOW"


def test_frozen_immutability():
    """All models are frozen (immutable)."""
    req = ResearchReportNodeRequest()
    with pytest.raises(FrozenInstanceError):
        req.request_id = "test"  # type: ignore

    resp = ResearchReportNodeResponse()
    with pytest.raises(FrozenInstanceError):
        resp.readonly_only = False  # type: ignore

    section = ResearchReportSection()
    with pytest.raises(FrozenInstanceError):
        section.readonly_only = False  # type: ignore
