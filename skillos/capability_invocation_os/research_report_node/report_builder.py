"""Research Report Node builder — main orchestrator class."""

import uuid

from skillos.capability_invocation_os.research_report_node.config import (
    is_research_report_node_enabled,
)
from skillos.capability_invocation_os.research_report_node.kill_switch import (
    should_force_disabled,
)
from skillos.capability_invocation_os.research_report_node.constants import (
    FORBIDDEN_REPORT_OUTPUTS,
    REPORT_NODE_MODE,
)
from skillos.capability_invocation_os.research_report_node.models import (
    ResearchReportDecision,
    ResearchReportNodeRequest,
    ResearchReportNodeResponse,
)
from skillos.capability_invocation_os.research_report_node.contracts import (
    validate_report_request,
    validate_b1_graph_response_for_report,
    validate_report_response,
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
from skillos.capability_invocation_os.research_report_node.evidence import (
    build_report_evidence_from_b1_graph,
    build_report_evidence_refs,
)
from skillos.capability_invocation_os.research_report_node.z9_snapshot import (
    build_z9_review_snapshot_candidate,
    build_z9_review_snapshot_candidate_from_report,
)


class ResearchReportNode:
    """Research Report Node — disabled by default in P0."""

    def __init__(self, fixture_mode: bool = False):
        self._fixture_mode = fixture_mode

    def _should_build_report(self) -> bool:
        """Determine if a report should be built."""
        if should_force_disabled():
            return False
        if not is_research_report_node_enabled():
            return False
        if not self._fixture_mode:
            return False
        return True

    def build_disabled_default_response(self) -> ResearchReportNodeResponse:
        """Build the default NOOP response."""
        return ResearchReportNodeResponse(
            response_id=str(uuid.uuid4()),
            decision=ResearchReportDecision.DISABLED_DEFAULT_NOOP,
            evidence={},
            sections=[],
            forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
            degraded=True,
            mode=REPORT_NODE_MODE,
            report_enabled=False,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            readonly_only=True,
            no_alpha_claim=True,
            no_trade_signal=True,
            no_position_weight=True,
        )

    def build_degraded_report(self, decision: ResearchReportDecision) -> ResearchReportNodeResponse:
        """Build a degraded report response."""
        return ResearchReportNodeResponse(
            response_id=str(uuid.uuid4()),
            decision=decision,
            evidence={},
            sections=[],
            forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
            degraded=True,
            mode=REPORT_NODE_MODE,
            report_enabled=False,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            readonly_only=True,
            no_alpha_claim=True,
            no_trade_signal=True,
            no_position_weight=True,
        )

    def build_report_from_b1_graph(
        self,
        b1_response,
        request: ResearchReportNodeRequest = None,
    ) -> ResearchReportNodeResponse:
        """Build full report from B1 CompositionGraphResponse."""
        if not self._should_build_report():
            return self.build_disabled_default_response()

        if request is None:
            request = ResearchReportNodeRequest()

        # Validate request
        req_decision = validate_report_request(request)
        if req_decision.value.startswith("DENY_"):
            return self.build_degraded_report(req_decision)

        # Validate B1 source
        b1_decision = validate_b1_graph_response_for_report(b1_response)
        if b1_decision == ResearchReportDecision.DENY_Z2_SOURCE_FORBIDDEN:
            return self.build_degraded_report(b1_decision)
        if b1_decision == ResearchReportDecision.DENY_Z2_REAL_SOURCE_FORBIDDEN:
            return self.build_degraded_report(b1_decision)
        if b1_decision == ResearchReportDecision.DENY_Z2_OUTPUTS_UNSAFE:
            return self.build_degraded_report(b1_decision)
        if b1_decision == ResearchReportDecision.DENY_Z2_EVIDENCE_INCOMPLETE:
            return self.build_degraded_report(b1_decision)

        # Build sections
        response_id = str(uuid.uuid4())
        sections = [
            build_report_header_section(),
            build_source_graph_summary_section(),
            build_factor_context_summary_section(),
            build_evidence_chain_summary_section(),
            build_structural_readiness_summary_section(),
            build_research_interpretation_section(),
            build_risk_warning_section(),
            build_missing_evidence_section(),
            build_blocked_outputs_removed_section(),
            build_confidence_section(),
            build_next_validation_requirement_section(),
        ]

        # Build evidence
        evidence = build_report_evidence_from_b1_graph(b1_response, response_id)

        # Build Z9 snapshot from report
        evidence_refs = build_report_evidence_refs(sections)
        z9_candidate = build_z9_review_snapshot_candidate_from_report(
            report_response=None,  # not yet built
            sections=sections,
            evidence=evidence,
        )

        # Determine final decision
        final_decision = b1_decision

        response = ResearchReportNodeResponse(
            response_id=response_id,
            decision=final_decision,
            evidence={"report_evidence": evidence, "z9_candidate": z9_candidate},
            sections=sections,
            forbidden_outputs_removed=sorted(FORBIDDEN_REPORT_OUTPUTS),
            degraded=(final_decision == ResearchReportDecision.ALLOW_Z2_DEGRADED_REPORT),
            mode=REPORT_NODE_MODE,
            report_enabled=True,
            runtime_enabled=False,
            adapter_execution_enabled=False,
            capability_execution_enabled=False,
            readonly_only=True,
            no_alpha_claim=True,
            no_trade_signal=True,
            no_position_weight=True,
        )

        # Validate response before return
        validation_decision = validate_report_response(response)
        if validation_decision.value.startswith("DENY_"):
            return self.build_degraded_report(validation_decision)

        return response
