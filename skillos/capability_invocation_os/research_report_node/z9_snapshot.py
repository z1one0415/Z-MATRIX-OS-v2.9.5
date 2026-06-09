"""Research Report Node Z9 review snapshot candidate builder."""

import hashlib
import json

from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    ResearchReportEvidence,
    Z9ReviewSnapshotCandidate,
)


def _snapshot_hash(data: str) -> str:
    """Produce a stable SHA-256 hex digest for snapshot fields."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_z9_review_snapshot_candidate(
    report_node_id: str = "",
    source_graph_hash: str = "",
    factor_context_summary_hash: str = "",
    evidence_chain_hash: str = "",
    research_summary_hash: str = "",
    risk_warning_hash: str = "",
    confidence_level: str = "LOW",
    confidence_reason: str = "",
    missing_evidence: list = None,
    degradation_status: str = "",
    review_required: bool = False,
    review_reason: str = "",
) -> Z9ReviewSnapshotCandidate:
    """Build a Z9ReviewSnapshotCandidate. Never raises."""
    return Z9ReviewSnapshotCandidate(
        report_node_id=report_node_id,
        source_graph_hash=source_graph_hash,
        factor_context_summary_hash=factor_context_summary_hash,
        evidence_chain_hash=evidence_chain_hash,
        research_summary_hash=research_summary_hash,
        risk_warning_hash=risk_warning_hash,
        confidence_level=confidence_level if confidence_level in ("LOW", "MEDIUM", "HIGH_WITH_STRUCTURE_ONLY") else "LOW",
        confidence_reason=confidence_reason,
        missing_evidence=missing_evidence or [],
        degradation_status=degradation_status,
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        review_required=review_required,
        review_reason=review_reason,
        readonly_only=True,
        no_trade_result=True,
        no_paper_trading=True,
        no_broker_action=True,
        no_position_change=True,
    )


def build_z9_review_snapshot_candidate_from_report(
    report_response=None,
    sections=None,
    evidence=None,
) -> Z9ReviewSnapshotCandidate:
    """Build snapshot from actual report response, not empty shell."""
    sections = sections or []
    missing_evidence_list = []

    # Determine report_node_id
    report_node_id = ""
    if report_response is not None:
        report_node_id = getattr(report_response, "response_id", "")

    # Source graph hash from evidence
    source_graph_hash = ""
    evidence_chain_hash = ""
    if isinstance(evidence, ResearchReportEvidence):
        if evidence.graph_node_hash and evidence.graph_edge_hash:
            source_graph_hash = _snapshot_hash(json.dumps(
                {"node": evidence.graph_node_hash, "edge": evidence.graph_edge_hash},
                sort_keys=True,
            ))
        else:
            missing_evidence_list.append("source_graph_hash")
        # evidence_chain_hash from evidence content
        evidence_chain_hash = _snapshot_hash(json.dumps({
            "request_hash": evidence.request_hash,
            "response_hash": evidence.response_hash_placeholder,
            "factor_decision_hash": evidence.factor_decision_hash,
            "bridge_decision_hash": evidence.bridge_decision_hash,
        }, sort_keys=True))
        if not evidence.factor_decision_hash:
            missing_evidence_list.append("factor_decision_hash")
        if not evidence.bridge_decision_hash:
            missing_evidence_list.append("bridge_decision_hash")
    elif isinstance(evidence, dict):
        gh = evidence.get("graph_node_hash", "")
        eh = evidence.get("graph_edge_hash", "")
        if gh and eh:
            source_graph_hash = _snapshot_hash(json.dumps({"node": gh, "edge": eh}, sort_keys=True))
        else:
            missing_evidence_list.append("source_graph_hash")
        evidence_chain_hash = _snapshot_hash(json.dumps({
            "request_hash": evidence.get("request_hash", ""),
            "response_hash": evidence.get("response_hash_placeholder", ""),
            "factor_decision_hash": evidence.get("factor_decision_hash", ""),
            "bridge_decision_hash": evidence.get("bridge_decision_hash", ""),
        }, sort_keys=True))
    else:
        missing_evidence_list.append("source_graph_hash")
        missing_evidence_list.append("evidence_chain")

    # Compute hashes from sections
    factor_context_summary_hash = ""
    research_summary_hash = ""
    risk_warning_hash = ""
    confidence_level = "LOW"

    for section in sections:
        stype = getattr(section, "section_type", "")
        sid = getattr(section, "section_id", "")
        if stype == "factor_context_summary":
            factor_context_summary_hash = _snapshot_hash(json.dumps(
                {"section_id": sid, "type": stype}, sort_keys=True,
            ))
        elif stype == "research_interpretation":
            research_summary_hash = _snapshot_hash(json.dumps(
                {"section_id": sid, "type": stype}, sort_keys=True,
            ))
        elif stype == "risk_warning":
            risk_warning_hash = _snapshot_hash(json.dumps(
                {"section_id": sid, "type": stype}, sort_keys=True,
            ))
        elif stype == "confidence_section":
            confidence_level = getattr(section, "confidence_level", "LOW")

    # Degradation
    degradation_status = ""
    if report_response is not None:
        degradation_status = "degraded" if getattr(report_response, "degraded", False) else ""

    # Review required if evidence incomplete
    review_required = len(missing_evidence_list) > 0
    review_reason = ""
    if review_required:
        review_reason = f"missing: {', '.join(missing_evidence_list)}"

    return Z9ReviewSnapshotCandidate(
        report_node_id=report_node_id,
        source_graph_hash=source_graph_hash,
        factor_context_summary_hash=factor_context_summary_hash,
        evidence_chain_hash=evidence_chain_hash,
        research_summary_hash=research_summary_hash,
        risk_warning_hash=risk_warning_hash,
        confidence_level=confidence_level if confidence_level in ("LOW", "MEDIUM", "HIGH_WITH_STRUCTURE_ONLY") else "LOW",
        confidence_reason=f"confidence from sections: {confidence_level}",
        missing_evidence=missing_evidence_list,
        degradation_status=degradation_status,
        blocked_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
        review_required=review_required,
        review_reason=review_reason,
        readonly_only=True,
        no_trade_result=True,
        no_paper_trading=True,
        no_broker_action=True,
        no_position_change=True,
    )


def validate_z9_review_snapshot_candidate(
    candidate: Z9ReviewSnapshotCandidate,
) -> ResearchReportDecision:
    """Validate a Z9ReviewSnapshotCandidate. Never raises."""
    if not isinstance(candidate, Z9ReviewSnapshotCandidate):
        return ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN
    if not candidate.readonly_only:
        return ResearchReportDecision.DENY_Z2_EXECUTION_FORBIDDEN
    if not candidate.no_trade_result:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not candidate.no_paper_trading:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not candidate.no_broker_action:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    if not candidate.no_position_change:
        return ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE
    return ResearchReportDecision.ALLOW_Z2_READONLY_REPORT
