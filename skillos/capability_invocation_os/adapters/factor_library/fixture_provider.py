"""Fixture Provider — reads only from in-memory fixtures. No real sources. No research."""

import uuid

from skillos.capability_invocation_os.adapters.factor_library.fixtures import (
    ALL_FIXTURE_SCENARIOS,
    FIXTURE_SCENARIO_MAP,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorManifestView,
    FactorInvocationResponse,
    FactorAdapterDecision,
    FactorEvidenceEnvelopeView,
)
from skillos.capability_invocation_os.adapters.factor_library.evidence import (
    build_c1_evidence_handoff,
    build_fixture_evidence,
)
from skillos.capability_invocation_os.adapters.factor_library.output_filter import (
    remove_forbidden_outputs,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS


class FactorLibraryFixtureProvider:
    """Provides fixture-based factor data. All in-memory. No real source reads."""

    def _build_response(self, scenario, decision=None) -> FactorInvocationResponse:
        """Build a FactorInvocationResponse from a fixture scenario."""
        effective_decision = decision if decision is not None else scenario.expected_decision
        evidence_dict = build_fixture_evidence(scenario)
        evidence_view = FactorEvidenceEnvelopeView(
            source_commit=evidence_dict["fixture_source_commit"],
            request_hash=evidence_dict["request_hash"],
            decision_hash=evidence_dict["decision_hash"],
            factor_manifest_hash=evidence_dict["factor_manifest_hash"],
            validation_snapshot_hash=evidence_dict["validation_snapshot_hash"],
            permission_tier=evidence_dict["permission_tier"],
            source_class=evidence_dict["source_class"],
            rollback_marker=evidence_dict["rollback_marker"],
        )
        # Remove forbidden outputs from any context data
        sample_data = {"factor_id": scenario.factor_id, "status": "fixture"}
        cleaned = remove_forbidden_outputs(sample_data)
        return FactorInvocationResponse(
            response_id=str(uuid.uuid4()),
            decision=effective_decision,
            evidence=evidence_view,
            forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
            degraded=scenario.expected_degraded_state,
        )

    def _deny_not_found(self, factor_id: str) -> FactorInvocationResponse:
        """Return DENY_FACTOR_NOT_FOUND for unknown factor_id."""
        return FactorInvocationResponse(
            response_id=str(uuid.uuid4()),
            decision=FactorAdapterDecision.DENY_FACTOR_NOT_FOUND,
            evidence=FactorEvidenceEnvelopeView(
                source_commit="P1_FIXTURE_ONLY",
                request_hash=f"not_found_{factor_id}",
                decision_hash="deny_not_found",
                factor_manifest_hash="",
                validation_snapshot_hash="",
                permission_tier="T0",
                source_class="factor_library_fixture",
            ),
            forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
            degraded=True,
        )

    def list_fixture_factors(self) -> FactorInvocationResponse:
        """Return list of all fixture manifests as a response."""
        # We return the first safe scenario's response for listing
        safe_scenario = ALL_FIXTURE_SCENARIOS[0]
        return self._build_response(
            safe_scenario,
            decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        )

    def get_fixture_profile(self, factor_id: str) -> FactorInvocationResponse:
        """Get fixture profile by factor_id."""
        scenario = FIXTURE_SCENARIO_MAP.get(factor_id)
        if scenario is None:
            return self._deny_not_found(factor_id)
        return self._build_response(scenario)

    def get_fixture_evidence(self, factor_id: str) -> FactorInvocationResponse:
        """Get fixture evidence by factor_id."""
        scenario = FIXTURE_SCENARIO_MAP.get(factor_id)
        if scenario is None:
            return self._deny_not_found(factor_id)
        return self._build_response(scenario)

    def monitor_fixture_candidates(self) -> FactorInvocationResponse:
        """Monitor all fixture candidates."""
        safe_scenario = ALL_FIXTURE_SCENARIOS[0]
        return self._build_response(
            safe_scenario,
            decision=FactorAdapterDecision.ALLOW_CANDIDATE_MONITOR,
        )

    def build_fixture_research_context(self, factor_id: str | None = None) -> FactorInvocationResponse:
        """Build fixture research context."""
        if factor_id is not None:
            scenario = FIXTURE_SCENARIO_MAP.get(factor_id)
            if scenario is None:
                return self._deny_not_found(factor_id)
            return self._build_response(scenario)
        # No specific factor -> return first safe scenario
        safe_scenario = ALL_FIXTURE_SCENARIOS[0]
        return self._build_response(
            safe_scenario,
            decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        )
