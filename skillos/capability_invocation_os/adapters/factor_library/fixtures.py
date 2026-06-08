"""P1 Fixture scenarios — in-memory only. No real factor reads. No research imports."""

from dataclasses import dataclass, field
from typing import List

from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorManifestView,
    FactorValidationSnapshotView,
    FactorGuardrailProfileView,
    FactorApplicationContractView,
    FactorEvidenceEnvelopeView,
    FactorAdapterDecision,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import BLOCKED_OUTPUTS


@dataclass(frozen=True)
class FixtureScenario:
    fixture_id: str
    factor_id: str
    factor_family_id: str
    manifest_view: FactorManifestView
    validation_snapshot_view: FactorValidationSnapshotView
    guardrail_profile_view: FactorGuardrailProfileView
    application_contract_view: FactorApplicationContractView
    evidence_envelope_view: FactorEvidenceEnvelopeView
    expected_decision: FactorAdapterDecision
    expected_forbidden_outputs_removed: List[str] = field(default_factory=lambda: list(BLOCKED_OUTPUTS))
    expected_degraded_state: bool = False
    expected_evidence_hashes: List[str] = field(default_factory=list)
    no_real_source_flag: bool = True
    fixture_source_commit: str = "P1_FIXTURE_ONLY"
    source_class: str = "factor_library_fixture"


# --- Scenario 1: Safe Validated ---
FIXTURE_FACTOR_SAFE_VALIDATED = FixtureScenario(
    fixture_id="FIXTURE_FACTOR_SAFE_VALIDATED",
    factor_id="FAKE_FACTOR_001",
    factor_family_id="FAKE_FAMILY_001",
    manifest_view=FactorManifestView(
        factor_id="FAKE_FACTOR_001",
        factor_name="Fake Safe Factor",
        factor_family_id="FAKE_FAMILY_001",
        factor_status="VALIDATED",
        factor_type="FIXTURE",
    ),
    validation_snapshot_view=FactorValidationSnapshotView(
        coverage_passed=True,
        pit_passed=True,
        promotion_allowed=False,
        alpha_claim_allowed=False,
        ready_for_candidate_review=True,
    ),
    guardrail_profile_view=FactorGuardrailProfileView(
        required_guardrails=["no_execution", "no_alpha"],
        guardrail_state="PASSED",
    ),
    application_contract_view=FactorApplicationContractView(
        allowed_application_modes=["READONLY"],
        blocked_application_modes=["EXECUTION"],
        blocked_outputs=list(BLOCKED_OUTPUTS),
        execution_requested=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
    ),
    evidence_envelope_view=FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="fixture_safe_001_req",
        decision_hash="fixture_safe_001_dec",
        factor_manifest_hash="fixture_safe_001_manifest",
        validation_snapshot_hash="fixture_safe_001_validation",
        permission_tier="T0",
        source_class="factor_library_fixture",
    ),
    expected_decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
)


# --- Scenario 2: Denied PIT Failed ---
FIXTURE_FACTOR_DENIED_PIT_FAILED = FixtureScenario(
    fixture_id="FIXTURE_FACTOR_DENIED_PIT_FAILED",
    factor_id="FAKE_FACTOR_002",
    factor_family_id="FAKE_FAMILY_002",
    manifest_view=FactorManifestView(
        factor_id="FAKE_FACTOR_002",
        factor_name="Fake PIT Failed Factor",
        factor_family_id="FAKE_FAMILY_002",
        factor_status="PIT_FAILED",
        factor_type="FIXTURE",
    ),
    validation_snapshot_view=FactorValidationSnapshotView(
        coverage_passed=True,
        pit_passed=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
        ready_for_candidate_review=False,
    ),
    guardrail_profile_view=FactorGuardrailProfileView(
        required_guardrails=["no_execution", "no_alpha"],
        guardrail_state="BLOCKED",
    ),
    application_contract_view=FactorApplicationContractView(
        allowed_application_modes=[],
        blocked_application_modes=["EXECUTION"],
        blocked_outputs=list(BLOCKED_OUTPUTS),
        execution_requested=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
    ),
    evidence_envelope_view=FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="fixture_pit_002_req",
        decision_hash="fixture_pit_002_dec",
        factor_manifest_hash="fixture_pit_002_manifest",
        validation_snapshot_hash="fixture_pit_002_validation",
        permission_tier="T0",
        source_class="factor_library_fixture",
    ),
    expected_decision=FactorAdapterDecision.DENY_PIT_FAILED,
)


# --- Scenario 3: Denied Coverage Failed ---
FIXTURE_FACTOR_DENIED_COVERAGE_FAILED = FixtureScenario(
    fixture_id="FIXTURE_FACTOR_DENIED_COVERAGE_FAILED",
    factor_id="FAKE_FACTOR_003",
    factor_family_id="FAKE_FAMILY_003",
    manifest_view=FactorManifestView(
        factor_id="FAKE_FACTOR_003",
        factor_name="Fake Coverage Failed Factor",
        factor_family_id="FAKE_FAMILY_003",
        factor_status="COVERAGE_FAILED",
        factor_type="FIXTURE",
    ),
    validation_snapshot_view=FactorValidationSnapshotView(
        coverage_passed=False,
        pit_passed=True,
        promotion_allowed=False,
        alpha_claim_allowed=False,
        ready_for_candidate_review=False,
    ),
    guardrail_profile_view=FactorGuardrailProfileView(
        required_guardrails=["no_execution", "no_alpha"],
        guardrail_state="BLOCKED",
    ),
    application_contract_view=FactorApplicationContractView(
        allowed_application_modes=[],
        blocked_application_modes=["EXECUTION"],
        blocked_outputs=list(BLOCKED_OUTPUTS),
        execution_requested=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
    ),
    evidence_envelope_view=FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="fixture_cov_003_req",
        decision_hash="fixture_cov_003_dec",
        factor_manifest_hash="fixture_cov_003_manifest",
        validation_snapshot_hash="fixture_cov_003_validation",
        permission_tier="T0",
        source_class="factor_library_fixture",
    ),
    expected_decision=FactorAdapterDecision.DENY_COVERAGE_FAILED,
)


# --- Scenario 4: Denied Guardrail Failed ---
FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED = FixtureScenario(
    fixture_id="FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED",
    factor_id="FAKE_FACTOR_004",
    factor_family_id="FAKE_FAMILY_004",
    manifest_view=FactorManifestView(
        factor_id="FAKE_FACTOR_004",
        factor_name="Fake Guardrail Failed Factor",
        factor_family_id="FAKE_FAMILY_004",
        factor_status="GUARDRAIL_FAILED",
        factor_type="FIXTURE",
    ),
    validation_snapshot_view=FactorValidationSnapshotView(
        coverage_passed=True,
        pit_passed=True,
        promotion_allowed=False,
        alpha_claim_allowed=False,
        ready_for_candidate_review=False,
    ),
    guardrail_profile_view=FactorGuardrailProfileView(
        required_guardrails=["no_execution", "no_alpha", "no_guardrail_bypass"],
        guardrail_state="FAILED",
    ),
    application_contract_view=FactorApplicationContractView(
        allowed_application_modes=[],
        blocked_application_modes=["EXECUTION"],
        blocked_outputs=list(BLOCKED_OUTPUTS),
        execution_requested=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
    ),
    evidence_envelope_view=FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="fixture_guard_004_req",
        decision_hash="fixture_guard_004_dec",
        factor_manifest_hash="fixture_guard_004_manifest",
        validation_snapshot_hash="fixture_guard_004_validation",
        permission_tier="T0",
        source_class="factor_library_fixture",
    ),
    expected_decision=FactorAdapterDecision.DENY_GUARDRAIL_FAILED,
)


# --- Scenario 5: Denied Promotion Not Allowed ---
FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED = FixtureScenario(
    fixture_id="FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED",
    factor_id="FAKE_FACTOR_005",
    factor_family_id="FAKE_FAMILY_005",
    manifest_view=FactorManifestView(
        factor_id="FAKE_FACTOR_005",
        factor_name="Fake Promotion Denied Factor",
        factor_family_id="FAKE_FAMILY_005",
        factor_status="PROMOTION_BLOCKED",
        factor_type="FIXTURE",
    ),
    validation_snapshot_view=FactorValidationSnapshotView(
        coverage_passed=True,
        pit_passed=True,
        promotion_allowed=False,
        alpha_claim_allowed=False,
        ready_for_candidate_review=False,
    ),
    guardrail_profile_view=FactorGuardrailProfileView(
        required_guardrails=["no_execution", "no_alpha"],
        guardrail_state="PASSED",
    ),
    application_contract_view=FactorApplicationContractView(
        allowed_application_modes=[],
        blocked_application_modes=["EXECUTION", "PROMOTION"],
        blocked_outputs=list(BLOCKED_OUTPUTS),
        execution_requested=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
    ),
    evidence_envelope_view=FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="fixture_promo_005_req",
        decision_hash="fixture_promo_005_dec",
        factor_manifest_hash="fixture_promo_005_manifest",
        validation_snapshot_hash="fixture_promo_005_validation",
        permission_tier="T0",
        source_class="factor_library_fixture",
    ),
    expected_decision=FactorAdapterDecision.DENY_PROMOTION_NOT_ALLOWED,
)


# --- Scenario 6: Denied Execution Forbidden ---
FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN = FixtureScenario(
    fixture_id="FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN",
    factor_id="FAKE_FACTOR_006",
    factor_family_id="FAKE_FAMILY_006",
    manifest_view=FactorManifestView(
        factor_id="FAKE_FACTOR_006",
        factor_name="Fake Execution Forbidden Factor",
        factor_family_id="FAKE_FAMILY_006",
        factor_status="EXECUTION_BLOCKED",
        factor_type="FIXTURE",
    ),
    validation_snapshot_view=FactorValidationSnapshotView(
        coverage_passed=True,
        pit_passed=True,
        promotion_allowed=False,
        alpha_claim_allowed=False,
        ready_for_candidate_review=False,
    ),
    guardrail_profile_view=FactorGuardrailProfileView(
        required_guardrails=["no_execution", "no_alpha", "no_broker"],
        guardrail_state="HARD_DENY",
    ),
    application_contract_view=FactorApplicationContractView(
        allowed_application_modes=[],
        blocked_application_modes=["EXECUTION", "BROKER", "REAL_TRADE"],
        blocked_outputs=list(BLOCKED_OUTPUTS),
        execution_requested=False,
        promotion_allowed=False,
        alpha_claim_allowed=False,
    ),
    evidence_envelope_view=FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="fixture_exec_006_req",
        decision_hash="fixture_exec_006_dec",
        factor_manifest_hash="fixture_exec_006_manifest",
        validation_snapshot_hash="fixture_exec_006_validation",
        permission_tier="T0",
        source_class="factor_library_fixture",
    ),
    expected_decision=FactorAdapterDecision.DENY_EXECUTION_FORBIDDEN,
)


# All fixture scenarios in a list for iteration
ALL_FIXTURE_SCENARIOS = [
    FIXTURE_FACTOR_SAFE_VALIDATED,
    FIXTURE_FACTOR_DENIED_PIT_FAILED,
    FIXTURE_FACTOR_DENIED_COVERAGE_FAILED,
    FIXTURE_FACTOR_DENIED_GUARDRAIL_FAILED,
    FIXTURE_FACTOR_DENIED_PROMOTION_NOT_ALLOWED,
    FIXTURE_FACTOR_DENIED_EXECUTION_FORBIDDEN,
]

# Map factor_id -> scenario for lookup
FIXTURE_SCENARIO_MAP = {s.factor_id: s for s in ALL_FIXTURE_SCENARIOS}
