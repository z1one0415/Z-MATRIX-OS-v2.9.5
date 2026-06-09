"""Tests for composition_graph.graph — CompositionGraphFactorBridge."""

from unittest.mock import patch

from skillos.capability_invocation_os.adapters.zmatrix_factor_bridge.models import (
    A1FactorBridgeResponse,
    A1FactorBridgeDecision,
    A1FactorBridgeEvidence,
)
from skillos.capability_invocation_os.composition_graph.constants import FORBIDDEN_GRAPH_OUTPUTS
from skillos.capability_invocation_os.composition_graph.graph import (
    CompositionGraphFactorBridge,
)
from skillos.capability_invocation_os.composition_graph.models import (
    CompositionGraphDecision,
    CompositionGraphResponse,
)


def _make_valid_response():
    return A1FactorBridgeResponse(
        response_id="test-123",
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,
        evidence=A1FactorBridgeEvidence(
            source_commit="P1_FIXTURE_ONLY",
            source_class="factor_library_fixture",
            no_real_source_flag=True,
            fixture_source_commit="P1_FIXTURE_ONLY",
            request_hash="test_req",
            response_hash_placeholder="test_resp",
            factor_decision_hash="test_factor",
            bridge_decision_hash="test_bridge",
            permission_tier="T0",
            forbidden_outputs_removed_hash="test_hash",
            rollback_marker=False,
            privacy_marker=True,
            c1_handoff_marker=True,
        ),
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        bridge_enabled=False,
        runtime_enabled=False,
        adapter_execution_enabled=False,
        capability_execution_enabled=False,
    )


def _make_denied_response():
    return A1FactorBridgeResponse(
        response_id="test-denied",
        decision=A1FactorBridgeDecision.DENY_BRIDGE_FACTOR_DENIED,
        evidence=A1FactorBridgeEvidence(
            source_commit="P1_FIXTURE_ONLY",
            source_class="factor_library_fixture",
            no_real_source_flag=True,
            fixture_source_commit="P1_FIXTURE_ONLY",
            request_hash="test_req",
            response_hash_placeholder="test_resp",
            factor_decision_hash="test_factor",
            bridge_decision_hash="test_bridge",
            permission_tier="T0",
            forbidden_outputs_removed_hash="test_hash",
            rollback_marker=False,
            privacy_marker=True,
            c1_handoff_marker=True,
        ),
        forbidden_outputs_removed=sorted(FORBIDDEN_GRAPH_OUTPUTS),
        degraded=True,
        mode="DISABLED_DEFAULT_P0",
        bridge_enabled=False,
        runtime_enabled=False,
        adapter_execution_enabled=False,
        capability_execution_enabled=False,
    )


def test_default_returns_disabled_noop():
    """Without mocking, kill switch is active → DISABLED_DEFAULT_NOOP."""
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_valid_response())
    assert isinstance(result, CompositionGraphResponse)
    assert result.decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP
    assert result.degraded is True


def test_none_response_returns_disabled_noop():
    """None a1_bridge_response → DISABLED_DEFAULT_NOOP."""
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(None)
    assert result.decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_valid_response_allows_readonly(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_valid_response())
    assert result.decision == CompositionGraphDecision.ALLOW_GRAPH_READONLY_SUMMARY
    assert result.degraded is False
    assert len(result.nodes) == 2
    assert len(result.edges) == 2


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_denied_bridge_response(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_denied_response())
    assert result.decision == CompositionGraphDecision.DENY_GRAPH_BRIDGE_DENIED
    assert result.degraded is True


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_invalid_type_denies_source(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process({"not": "valid"})
    assert result.decision == CompositionGraphDecision.DENY_GRAPH_SOURCE_FORBIDDEN


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_outputs_unsafe(mock_config, mock_kill):
    resp = A1FactorBridgeResponse(
        response_id="test-unsafe",
        decision=A1FactorBridgeDecision.ALLOW_BRIDGE_READONLY_CONTEXT,
        evidence=A1FactorBridgeEvidence(
            source_commit="P1_FIXTURE_ONLY",
            source_class="factor_library_fixture",
            no_real_source_flag=True,
            fixture_source_commit="P1_FIXTURE_ONLY",
            request_hash="r",
            response_hash_placeholder="r",
            factor_decision_hash="f",
            bridge_decision_hash="b",
            permission_tier="T0",
            forbidden_outputs_removed_hash="h",
            rollback_marker=False,
            privacy_marker=True,
            c1_handoff_marker=True,
        ),
        forbidden_outputs_removed=["alpha_claim"],  # incomplete
        degraded=False,
        mode="DISABLED_DEFAULT_P0",
        bridge_enabled=False,
        runtime_enabled=False,
        adapter_execution_enabled=False,
        capability_execution_enabled=False,
    )
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(resp)
    assert result.decision == CompositionGraphDecision.DENY_GRAPH_OUTPUTS_UNSAFE


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_not_fixture_mode_returns_disabled(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=False)
    result = bridge.process(_make_valid_response())
    assert result.decision == CompositionGraphDecision.DISABLED_DEFAULT_NOOP


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_response_has_forbidden_outputs_removed(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_valid_response())
    assert set(result.forbidden_outputs_removed) == FORBIDDEN_GRAPH_OUTPUTS


@patch("skillos.capability_invocation_os.composition_graph.graph.should_force_disabled", return_value=False)
@patch("skillos.capability_invocation_os.composition_graph.graph.is_composition_graph_enabled", return_value=True)
def test_response_id_prefixed(mock_config, mock_kill):
    bridge = CompositionGraphFactorBridge(fixture_mode=True)
    result = bridge.process(_make_valid_response())
    assert result.response_id.startswith("graph_")
