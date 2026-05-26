"""Approval Loop Event Adapters — build EventStore events (no auto-append)"""
from __future__ import annotations

from zmatrix.event_store.builders import build_event


def build_approval_request_event(approval_request: dict) -> dict:
    """Build a MemoryCandidateEvent from an approval request.

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    """
    payload = {
        "approval_request_id": approval_request.get("approval_request_id", ""),
        "request_version": approval_request.get("request_version", ""),
        "request_type": approval_request.get("request_type", ""),
        "source_preview_id": approval_request.get("source_preview_id", ""),
        "requested_by": approval_request.get("requested_by", ""),
        "status": approval_request.get("status", "PENDING_REVIEW"),
        "requires_human_approval": approval_request.get("requires_human_approval", True),
    }
    return build_event(
        event_type="MemoryCandidateEvent",
        producer_module="zmatrix.approval_loop.event_adapters.build_approval_request_event",
        payload=payload,
    )


def build_human_approval_event(approval_decision: dict) -> dict:
    """Build a HumanApprovalEvent from an approval decision.

    Does NOT append. Does NOT write Hermes memory. Does NOT write Z9.
    Does NOT enable auto calibration or prompt injection.
    """
    payload = {
        "approval_decision_id": approval_decision.get("approval_decision_id", ""),
        "decision_version": approval_decision.get("decision_version", ""),
        "approval_request_id": approval_decision.get("approval_request_id", ""),
        "decision": approval_decision.get("decision", ""),
        "result_status": approval_decision.get("result_status", ""),
        "human_operator": approval_decision.get("human_operator", ""),
        "rationale": approval_decision.get("rationale", ""),
    }
    return build_event(
        event_type="HumanApprovalEvent",
        producer_module="zmatrix.approval_loop.event_adapters.build_human_approval_event",
        payload=payload,
    )
