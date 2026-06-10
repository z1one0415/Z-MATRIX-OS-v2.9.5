"""Z9 Review Node builder — disabled-default P0 facade."""

import uuid
from skillos.capability_invocation_os.review_node.config import (
    is_z9_review_node_enabled,
)
from skillos.capability_invocation_os.review_node.kill_switch import (
    should_force_disabled,
)
from skillos.capability_invocation_os.review_node.constants import (
    FORBIDDEN_OUTPUT_KEYS,
    ALLOWED_REVIEW_SECTIONS,
    MODE,
)
from skillos.capability_invocation_os.review_node.models import (
    Z9ReviewDecision,
    Z9ReviewNodeRequest,
    Z9ReviewNodeResponse,
    Z9ReviewSection,
    Z2FeedbackCandidate,
)
from skillos.capability_invocation_os.review_node.contracts import (
    validate_z9_review_request,
    validate_z2_snapshot_candidate,
    validate_z9_review_response,
)
from skillos.capability_invocation_os.review_node.evidence import (
    build_z9_review_evidence_from_z2_snapshot,
    build_z9_review_node_hash,
    build_z9_review_section_hash,
    build_z9_feedback_candidate_hash,
)
from skillos.capability_invocation_os.review_node.z2_feedback import (
    build_z2_feedback_candidate,
)


class Z9ReviewNode:
    """Z9 Review Node — disabled by default in P0."""

    def __init__(self, fixture_mode: bool = False):
        self._fixture_mode = fixture_mode

    def _should_build_review(self) -> bool:
        if should_force_disabled():
            return False
        if not is_z9_review_node_enabled():
            return False
        if not self._fixture_mode:
            return False
        return True

    def build_disabled_default_response(self) -> Z9ReviewNodeResponse:
        return Z9ReviewNodeResponse(
            response_id=str(uuid.uuid4()),
            decision=Z9ReviewDecision.DISABLED_DEFAULT_NOOP,
            evidence={},
            sections=[],
            forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
            degraded=True,
            mode=MODE,
            review_enabled=False,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            memory_mutation_enabled=False,
            readonly_only=True,
            no_trade_result=True,
            no_paper_trading=True,
            no_broker_action=True,
            no_position_change=True,
        )

    def build_degraded_review(self, decision: Z9ReviewDecision) -> Z9ReviewNodeResponse:
        return Z9ReviewNodeResponse(
            response_id=str(uuid.uuid4()),
            decision=decision,
            evidence={},
            sections=[],
            forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
            degraded=True,
            mode=MODE,
            review_enabled=False,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            memory_mutation_enabled=False,
            readonly_only=True,
            no_trade_result=True,
            no_paper_trading=True,
            no_broker_action=True,
            no_position_change=True,
        )

    def _build_review_sections(self, response_id: str, snapshot) -> list:
        """Build the 12 review sections from a Z2 snapshot."""
        sections = []
        section_types = sorted(ALLOWED_REVIEW_SECTIONS)
        for i, stype in enumerate(section_types):
            section_id = f"{response_id}_sec_{i:02d}"
            section_hash = build_z9_review_section_hash(section_id, stype)
            section = Z9ReviewSection(
                section_id=section_id,
                section_type=stype,
                source_refs=[snapshot.report_node_id] if hasattr(snapshot, "report_node_id") else [],
                evidence_refs=[response_id],
                review_label="EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
                confidence_alignment_label=snapshot.confidence_level if hasattr(snapshot, "confidence_level") else "LOW",
                degradation_status=snapshot.degradation_status if hasattr(snapshot, "degradation_status") else "",
                blocked_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
                readonly_only=True,
            )
            sections.append(section)
        return sections

    def build_review_from_z2_snapshot(self, snapshot, request=None) -> Z9ReviewNodeResponse:
        if not self._should_build_review():
            return self.build_disabled_default_response()
        if request is None:
            request = Z9ReviewNodeRequest()
        req_decision = validate_z9_review_request(request)
        if req_decision.value.startswith("DENY_"):
            return self.build_degraded_review(req_decision)
        snap_decision = validate_z2_snapshot_candidate(snapshot)
        if snap_decision.value.startswith("DENY_"):
            return self.build_degraded_review(snap_decision)
        response_id = str(uuid.uuid4())
        # Build real evidence from Z2 snapshot
        evidence = build_z9_review_evidence_from_z2_snapshot(snapshot, response_id=response_id)
        # Build 12 review sections
        sections = self._build_review_sections(response_id, snapshot)
        # Compute review node hash
        node_hash = build_z9_review_node_hash(response_id, MODE)
        # Build z2 feedback candidate
        # First build a temporary response to derive the feedback
        temp_response = Z9ReviewNodeResponse(
            response_id=response_id,
            decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
            evidence=evidence,
            sections=sections,
            forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
            degraded=False,
            mode=MODE,
            review_enabled=True,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            memory_mutation_enabled=False,
            readonly_only=True,
            no_trade_result=True,
            no_paper_trading=True,
            no_broker_action=True,
            no_position_change=True,
        )
        z2_feedback = build_z2_feedback_candidate(temp_response)
        # Build final response with z2_feedback_candidate
        response = Z9ReviewNodeResponse(
            response_id=response_id,
            decision=Z9ReviewDecision.ALLOW_Z9_READONLY_REVIEW,
            evidence=evidence,
            sections=sections,
            z2_feedback_candidate=z2_feedback,
            forbidden_outputs_removed=sorted(FORBIDDEN_OUTPUT_KEYS),
            degraded=False,
            mode=MODE,
            review_enabled=True,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            memory_mutation_enabled=False,
            readonly_only=True,
            no_trade_result=True,
            no_paper_trading=True,
            no_broker_action=True,
            no_position_change=True,
        )
        validation = validate_z9_review_response(response)
        if validation.value.startswith("DENY_"):
            return self.build_degraded_review(validation)
        return response
