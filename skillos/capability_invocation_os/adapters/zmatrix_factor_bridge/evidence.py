import hashlib
import json

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeEvidence,
    A1FactorBridgeDecision,
)


def build_a1_bridge_request_hash(request) -> str:
    return hashlib.sha256(
        json.dumps(str(request), sort_keys=True).encode()
    ).hexdigest()


def build_a1_bridge_decision_hash(decision) -> str:
    if isinstance(decision, A1FactorBridgeDecision):
        value = decision.value
    else:
        value = str(decision)
    return hashlib.sha256(value.encode()).hexdigest()


def build_a1_bridge_evidence(response) -> A1FactorBridgeEvidence:
    """Build evidence from a bridge response."""
    request_hash = ""
    response_hash_placeholder = ""
    factor_decision_hash = ""
    bridge_decision_hash = ""
    forbidden_outputs_removed_hash = ""

    if isinstance(response.decision, A1FactorBridgeDecision):
        bridge_decision_hash = build_a1_bridge_decision_hash(response.decision)

    forbidden_outputs_removed_hash = hashlib.sha256(
        json.dumps(sorted(response.forbidden_outputs_removed)).encode()
    ).hexdigest()

    return A1FactorBridgeEvidence(
        source_commit="P1_FIXTURE_ONLY",
        source_class="factor_library_fixture",
        no_real_source_flag=True,
        fixture_source_commit="P1_FIXTURE_ONLY",
        request_hash=request_hash,
        response_hash_placeholder=response_hash_placeholder,
        factor_decision_hash=factor_decision_hash,
        bridge_decision_hash=bridge_decision_hash,
        permission_tier="T0",
        forbidden_outputs_removed_hash=forbidden_outputs_removed_hash,
        rollback_marker=False,
        privacy_marker=True,
        c1_handoff_marker=True,
    )


def build_a1_bridge_c1_handoff(response) -> dict:
    """Build C1 handoff dict from a bridge response."""
    evidence = build_a1_bridge_evidence(response)
    return {
        "source_class": evidence.source_class,
        "no_real_source_flag": evidence.no_real_source_flag,
        "fixture_source_commit": evidence.fixture_source_commit,
        "request_hash": evidence.request_hash,
        "response_hash_placeholder": evidence.response_hash_placeholder,
        "factor_decision_hash": evidence.factor_decision_hash,
        "bridge_decision_hash": evidence.bridge_decision_hash,
        "permission_tier": evidence.permission_tier,
        "forbidden_outputs_removed_hash": evidence.forbidden_outputs_removed_hash,
        "rollback_marker": evidence.rollback_marker,
        "privacy_marker": evidence.privacy_marker,
        "c1_handoff_marker": evidence.c1_handoff_marker,
    }
