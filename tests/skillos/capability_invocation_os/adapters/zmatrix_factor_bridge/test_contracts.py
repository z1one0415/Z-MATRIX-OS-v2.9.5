import pytest
import uuid
from unittest.mock import MagicMock

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.contracts import (
    validate_bridge_request,
    validate_factor_response_for_bridge,
    validate_no_forbidden_outputs,
    validate_no_real_source,
)
from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeRequest,
    A1FactorBridgeDecision,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.adapters.factor_library.models import (
    FactorInvocationResponse,
    FactorAdapterDecision,
    FactorEvidenceEnvelopeView,
)
from skillos.capability_invocation_os.adapters.factor_library.constants import (
    BLOCKED_OUTPUTS,
)


def _make_fixture_response(
    decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
    source_class="factor_library_fixture",
    forbidden_outputs_removed=None,
    evidence_kwargs=None,
):
    """Helper to build a FactorInvocationResponse for bridge validation."""
    if forbidden_outputs_removed is None:
        forbidden_outputs_removed = list(BLOCKED_OUTPUTS)

    evidence = FactorEvidenceEnvelopeView(
        source_commit="P1_FIXTURE_ONLY",
        request_hash="test_req",
        decision_hash="test_dec",
        factor_manifest_hash="test_manifest",
        validation_snapshot_hash="test_validation",
        permission_tier="T0",
        source_class=source_class,
        rollback_marker=False,
        **(evidence_kwargs or {}),
    )

    return FactorInvocationResponse(
        response_id=str(uuid.uuid4()),
        decision=decision,
        evidence=evidence,
        forbidden_outputs_removed=forbidden_outputs_removed,
        degraded=False,
    )


def test_fixture_response_accepted():
    resp = _make_fixture_response()
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT


def test_source_class_unknown_denied():
    resp = _make_fixture_response(source_class="research_live")
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN


def test_no_real_source_flag_false_denied():
    """Use a mock to simulate evidence with no_real_source_flag=False."""
    resp = MagicMock()
    resp.decision = FactorAdapterDecision.ALLOW_READONLY_CONTEXT
    resp.forbidden_outputs_removed = list(BLOCKED_OUTPUTS)

    mock_evidence = MagicMock()
    mock_evidence.source_class = "factor_library_fixture"
    mock_evidence.no_real_source_flag = False
    resp.evidence = mock_evidence

    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN


def test_missing_forbidden_output_denied():
    resp = _make_fixture_response(forbidden_outputs_removed=["buy_signal"])
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE


def test_deny_factor_response_denied():
    resp = _make_fixture_response(decision=FactorAdapterDecision.DENY_PIT_FAILED)
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED


def test_execution_requested_denied():
    req = A1FactorBridgeRequest(
        request_id="test",
        execution_requested=True,
        source_class="factor_library_fixture",
    )
    result = validate_bridge_request(req)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_EXECUTION_FORBIDDEN


def test_alpha_trade_weight_fields_in_payload_denied():
    payload = {"alpha_claim": 0.05, "buy_signal": True}
    result = validate_no_forbidden_outputs(payload)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE


def test_source_forbidden_not_collapsed_to_factor_denied():
    """Source class unknown must return DENY_BRIDGE_SOURCE_FORBIDDEN, NOT factor denied."""
    resp = _make_fixture_response(source_class="research_live")
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_SOURCE_FORBIDDEN
    assert result != A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED


def test_real_source_forbidden_not_collapsed_to_factor_denied():
    """no_real_source_flag false must return DENY_BRIDGE_REAL_SOURCE_FORBIDDEN."""
    resp = MagicMock()
    resp.decision = FactorAdapterDecision.ALLOW_READONLY_CONTEXT
    resp.forbidden_outputs_removed = list(BLOCKED_OUTPUTS)
    mock_evidence = MagicMock()
    mock_evidence.source_class = "factor_library_fixture"
    mock_evidence.no_real_source_flag = False
    resp.evidence = mock_evidence

    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN
    assert result != A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED


def test_outputs_unsafe_not_collapsed_to_factor_denied():
    """Missing forbidden output must return DENY_BRIDGE_OUTPUTS_UNSAFE, NOT factor denied."""
    resp = _make_fixture_response(forbidden_outputs_removed=["buy_signal"])
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_OUTPUTS_UNSAFE
    assert result != A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED


def test_factor_deny_maps_to_factor_denied_only_after_safety_checks_pass():
    """Factor DENY_PIT_FAILED with safe source/output must return DENY_BRIDGE_FACTOR_DENIED."""
    resp = _make_fixture_response(decision=FactorAdapterDecision.DENY_PIT_FAILED)
    result = validate_factor_response_for_bridge(resp)
    # Source and output checks pass, so factor denial is correctly identified
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED


def test_evidence_none_denies_real_source():
    """Response with evidence=None must return DENY_BRIDGE_REAL_SOURCE_FORBIDDEN."""
    resp = FactorInvocationResponse(
        response_id=str(uuid.uuid4()),
        decision=FactorAdapterDecision.ALLOW_READONLY_CONTEXT,
        evidence=None,
        forbidden_outputs_removed=list(BLOCKED_OUTPUTS),
    )
    result = validate_factor_response_for_bridge(resp)
    assert result == A1FactorBridgeDecision.DENY_BRIDGE_REAL_SOURCE_FORBIDDEN
