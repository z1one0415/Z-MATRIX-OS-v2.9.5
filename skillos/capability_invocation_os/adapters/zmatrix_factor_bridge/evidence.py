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


def build_a1_bridge_evidence(response, source_factor_response=None) -> A1FactorBridgeEvidence:
    """Build evidence from a bridge response, inheriting from source factor response.

    When source_factor_response is provided, key evidence fields are
    inherited, preserving no_real_source_flag and P1_FIXTURE_ONLY markers.
    When absent, disabled-default placeholder values are used.
    """
    # Inherit or default
    source_class = "factor_library_disabled_default"
    no_real_source_flag = True
    fixture_source_commit = "DISABLED_DEFAULT"
    request_hash = ""
    response_hash_placeholder = ""
    factor_decision_hash = ""
    permission_tier = "T0"
    rollback_marker = False
    privacy_marker = True

    if source_factor_response is not None and source_factor_response.evidence is not None:
        se = source_factor_response.evidence
        source_class = getattr(se, 'source_class', source_class)
        no_real_source_flag = getattr(se, 'no_real_source_flag', no_real_source_flag)
        fixture_source_commit = getattr(se, 'source_commit', fixture_source_commit) or fixture_source_commit
        if getattr(se, 'fixture_source_commit', None):
            fixture_source_commit = se.fixture_source_commit
        request_hash = getattr(se, 'request_hash', request_hash) or request_hash
        response_hash_placeholder = getattr(se, 'response_hash_placeholder', response_hash_placeholder) or response_hash_placeholder
        permission_tier = getattr(se, 'permission_tier', permission_tier) or permission_tier
        rollback_marker = getattr(se, 'rollback_marker', rollback_marker)
        privacy_marker = getattr(se, 'privacy_marker', privacy_marker)
        # Hash source factor decision
        if hasattr(source_factor_response, 'decision'):
            factor_decision_hash = hashlib.sha256(
                source_factor_response.decision.value.encode()
            ).hexdigest()

    bridge_decision_hash = ""
    if isinstance(response.decision, A1FactorBridgeDecision):
        bridge_decision_hash = build_a1_bridge_decision_hash(response.decision)

    forbidden_outputs_removed_hash = hashlib.sha256(
        json.dumps(sorted(response.forbidden_outputs_removed)).encode()
    ).hexdigest()

    return A1FactorBridgeEvidence(
        source_commit=fixture_source_commit,
        source_class=source_class,
        no_real_source_flag=no_real_source_flag,
        fixture_source_commit=fixture_source_commit,
        request_hash=request_hash,
        response_hash_placeholder=response_hash_placeholder,
        factor_decision_hash=factor_decision_hash,
        bridge_decision_hash=bridge_decision_hash,
        permission_tier=permission_tier,
        forbidden_outputs_removed_hash=forbidden_outputs_removed_hash,
        rollback_marker=rollback_marker,
        privacy_marker=privacy_marker,
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
