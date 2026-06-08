"""Evidence — hash-only, in-memory, no file writes. C1 handoff fields present."""

import hashlib
import json

from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorEvidenceEnvelopeView,
    FactorAdapterDecision,
)


def build_request_hash(request) -> str:
    return hashlib.sha256(json.dumps(str(request), sort_keys=True).encode()).hexdigest()


def build_response_hash_placeholder() -> str:
    return "response_hash_placeholder_p0"


def build_decision_hash(decision: FactorAdapterDecision) -> str:
    return hashlib.sha256(decision.value.encode()).hexdigest()


def build_factor_evidence_view(
    source_commit: str = "",
    request_hash: str = "",
    decision_hash: str = "",
    factor_manifest_hash: str = "",
    validation_snapshot_hash: str = "",
    permission_tier: str = "T0",
    source_class: str = "factor_library",
) -> FactorEvidenceEnvelopeView:
    return FactorEvidenceEnvelopeView(
        source_commit=source_commit,
        request_hash=request_hash,
        decision_hash=decision_hash,
        factor_manifest_hash=factor_manifest_hash,
        validation_snapshot_hash=validation_snapshot_hash,
        permission_tier=permission_tier,
        source_class=source_class,
    )


def build_c1_evidence_handoff(
    request_hash: str,
    decision_hash: str,
    factor_manifest_hash: str = "p0_placeholder",
    validation_snapshot_hash: str = "p0_placeholder",
    source_commit: str = "p0_placeholder",
    source_class: str = "factor_library",
    permission_tier: str = "T0",
) -> dict:
    return {
        "source_commit": source_commit,
        "request_hash": request_hash,
        "response_hash_placeholder": build_response_hash_placeholder(),
        "decision_hash": decision_hash,
        "factor_manifest_hash": factor_manifest_hash,
        "validation_snapshot_hash": validation_snapshot_hash,
        "guardrail_profile_hash": "p0_placeholder",
        "application_contract_hash": "p0_placeholder",
        "permission_tier": permission_tier,
        "source_class": source_class,
        "rollback_marker": False,
        "privacy_marker": True,
    }


def build_fixture_evidence(fixture_scenario) -> dict:
    """Build evidence dict from a fixture scenario. P1 fixture layer only."""
    request_hash = hashlib.sha256(
        json.dumps({"fixture_id": fixture_scenario.fixture_id}).encode()
    ).hexdigest()
    decision_hash = hashlib.sha256(
        fixture_scenario.expected_decision.value.encode()
    ).hexdigest()
    factor_manifest_hash = hashlib.sha256(
        fixture_scenario.fixture_id.encode()
    ).hexdigest()
    validation_snapshot_hash = hashlib.sha256(
        f"{fixture_scenario.fixture_id}_validation".encode()
    ).hexdigest()
    guardrail_profile_hash = hashlib.sha256(
        f"{fixture_scenario.fixture_id}_guardrail".encode()
    ).hexdigest()
    application_contract_hash = hashlib.sha256(
        f"{fixture_scenario.fixture_id}_contract".encode()
    ).hexdigest()

    return {
        "fixture_source_commit": "P1_FIXTURE_ONLY",
        "source_class": "factor_library_fixture",
        "request_hash": request_hash,
        "response_hash_placeholder": build_response_hash_placeholder(),
        "decision_hash": decision_hash,
        "factor_manifest_hash": factor_manifest_hash,
        "validation_snapshot_hash": validation_snapshot_hash,
        "guardrail_profile_hash": guardrail_profile_hash,
        "application_contract_hash": application_contract_hash,
        "permission_tier": "T0",
        "rollback_marker": False,
        "privacy_marker": True,
        "no_real_source_flag": True,
    }
